# Scope Architecture

The repository provides **two independent pipelines** for building call graphs:

- **LSP-based call graph** (high-fidelity, language-server driven)

entry-point → `scope/callgraph/api/CallGraph.py`
- **Tree-sitter “approximate” call graph** (fast, heuristic)

entry-point → `scope/callgraph/treesitter.py`

The first approach provides **high-quality edges** (it asks a language-server for the *ground-truth* definition → reference relations, or more accurately, the LSP's best guess. Sometimes this is incomplete, like JEDI language server for Python being unable to resolve aliases of aliases).  

The second approach is **self-contained & very fast** (no external servers, works even when LSPs are flaky) and is a pragmatic good-enough solution when the result (ApproximateCallGraph) is used as one tool in codebase RAG.

---

## 1. LSP-based CallGraph (`CallGraph`)

### 1.1 Basic Overview

1. **File system split** – `copy_and_split_root_by_language_group()` makes a *temporary* copy of the repository **per language** (Python / TS / Go …).  This enables us to run a *language-specific* LSP instance against each subtree.
2. **Symbol discovery** – `CallGraphBuilder.find_definitions()` requests `textDocument/documentSymbol` for every file.  Returned LSP Symbol information is wrapped in our own `Symbol` DTO.
3. **Definition resolution** – every `Symbol` is converted into a `Definition` via `Symbol.to_definition()` (under the hood it issues `textDocument/definition`) Symbols/definitions will be excluded if lookup fails.
4. **Reference resolution** – for each `Definition` we execute `textDocument/references` (see `Definition.resolve_references()`), producing raw LSP reference locations.
5. **Parent/child wiring** – `CallGraphBuilder.mark_references_for_path()` maps raw locations back to *enclosing* definitions (`get_containing_def_for_ref`) so that we can populate:
   * `definition.referenced_by   # callers`
   * `definition.referencing    # callees`
6. **Object Construction** – `CallGraphBuilder.generate_callgraph()` converts absolute paths → relative ones and returns a `Dict[str, List[Definition]]` that is finally wrapped by `CallGraph` object.


```text
CallGraph.build(root_path)                 # api/CallGraph.py
├─ copy_and_split_root_by_language_group() # utils.py
│    • Clones project once per language
│    • Filters out non-pertinent files
└─ ∀ (cloned_path, language):
     CallGraphBuilder.generate_callgraph() # builder.py
     └─ find_definitions()   (LSP)
     │   ├─ request_document_symbols()
     │   ├─ Symbol  → Definition DTO
     │   └─ potential_aliases (imports)
     ├─ mark_references()     (LSP)
     │   ├─ Definition.resolve_references()
     │   ├─ Parent/child linking via Reference DTOs
     │   └─ Alias resolution (optional)
     └─ post-process paths → relative
        return {file_path: [Definition, …]}
CallGraph(...)
```

### 1.2 Key classes

| File | Class | Responsibility |
|------|-------|----------------|
| `builder.py` | `CallGraphBuilder` | Orchestrates the 6-step pipeline above |
| `api/CallGraph.py` | `CallGraph` | Thin wrapper around the python `dict` representation, offers traversal, merging, visualisation |
| `dtos/*.py` | `Definition`, `Reference`, `Symbol`, `Alias` | Encapsulates complexity of LSP results and normalizes data to lang-agnostic interface |

### 1.3 Configuration (`CallGraphBuilderConfig`)

```python
CallGraphBuilderConfig(
    timeit=False,
    allowed_symbols="strict", # filter out non-code (comments, strings …) see allowed enums
    allow_libraries=False, # keep/ignore third-party deps
    retain_symbols=False   # keep raw Symbols alongside Definitions
)
```

All options can be *OR-combined* (`cfg1 | cfg2`) – RHS overrides LHS.

### 1.4 Notes and Tradeoffs

- 100 % accurate – uses the compiler/IDE tooling itself.  
- Handles dynamic language features (re-exports, imports, overloads) when the LSP supports them.  
- Requires a fully-functional LSP per language (may be heavy / flaky).  
- Spin-up latency (needs to copy repo & warm language servers).
- Performance ultimately dependent on underlying LSP implementation.

---

## 2. Tree-Sitter Approximate CallGraph (`ApproximateCallGraph`)

### 2.1 Motivation
Often you *cannot* or *do not want to* run an LSP (mono-repos with dozens of languages, air-gapped environments, CI where LSPs crash).  Building an approximate callgraph lets us parse source files locally and very fast – we trade some precision for relative universality and speed.

### 2.2 Pipeline

1. **Parse phase** – `ScopeASTBuilder` walks every file and executes language-specific Tree-Sitter **queries** defined in `resources/tree_sitter`.  Matches are turned into `ASTNode`s labelled either `definition` or `reference`.
2. **Range bookkeeping** – each `ASTNode` stores `name_range` & `code_range` for later wiring/backtracking.
3. **Reference → definition backtracking**
   * For a reference `R` we first look for a matching definition *in the same file*.
   * If none is found we broaden to other files with the same name & language (`backtrack_ref_to_origin_defs`).
   * Ambiguity is capped by `BACKTRACK_LIMIT` (defaults to 2).
4. **Basic Pruning** – `ApproximateCallGraphBuilder.prune_refs()` drops obvious false positives (self-cycles, identically-named siblings in same file).
5. **Graph construction** – nodes + edges are batch-added to a `rustworkx.PyDiGraph`; cycles are removed so that downstream algorithms (Leiden clustering, longest path etc.) can assume a DAG.
6. **Some higher-level features** – the resulting `ApproximateCallGraph` provides:
   * `to_igraph()` – convert to igraph for community detection.
   * `longest_path()` – rough entry-point to deepest call-stacks.
   * `indexing_queue()` – orders nodes for Just-In-Time (JIT) indexing based on Leiden communities & centrality.

```text
ApproximateCallGraph.build(files)
├─ ScopeASTBuilder(files)
│   ├─ parse → ASTNode(definition / reference)
├─ ApproximateCallGraphBuilder(ast)
│   ├─ _mark_references()    # heuristic linking
│   ├─ prune_refs()
│   ├─ rustworkx.PyDiGraph construction
│   └─ _remove_cycles()
└─ return ApproximateCallGraph(...)
```

### 2.3 Configuration

* `BACKTRACK_LIMIT` – max number of candidate definitions to attach to an ambiguous reference.
* `prune_references` (bool) – toggle heuristic pruning step.
* `timeit`, `progress_bar` – useful for debugging performance issues.

### 2.4 Notes and Tradeoffs
- Zero external dependencies
- Practically infinitely scalable (indexes K8s in less than 2 minutes)
- Easy to extend, if there's a tree-sitter parser - just add new queries to `resources/tree_sitter`
- Heuristic – may miss dynamic dispatch, decorators, runtime indirection.  
- Cannot follow re-exports/import-aliasing across packages reliably.

---

## 3. Choosing the right callgraph builder

| Need | Recommendation |
|------|----------------|
|Maximum accuracy & latency-insensitive | CallGraph |
| Works everywhere or prototyping | ApproximateCallGraph |
| Incremental re-indexing | Either – both will expose `CallGraph.update()` soon |


---

## 4. File layout cheat-sheet

```text
scope/
  callgraph/
    api/CallGraph.py              # LSP CG 
    builder.py                    # LSP CG builder
    constants.py, utils.py        # helpers & language maps
    treesitter.py                 # ScopeAST + ApproximateCallGraph
    resources/
      tree_sitter/                # ts queries grouped by language
    dtos/                         # Definition, Reference, Symbol …
    enums/                        # tiny enums used across both engines
```
