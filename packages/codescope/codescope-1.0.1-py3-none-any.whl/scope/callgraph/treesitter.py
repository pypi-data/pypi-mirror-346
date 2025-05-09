# Standard library
import os
import time
from collections import defaultdict
from typing import List, Dict, Callable, Tuple, Literal, Set
from functools import cache, cached_property

# Local
from scope.callgraph.dtos.Range import Range
from withrepo import RepoFile, File
from scope.callgraph.enums.TreeSitterNodeVariant import TreeSitterNodeVariant
from scope.callgraph.resources.tree_sitter import (
    TREE_SITTER_REF_DEF_QUERIES,
    EXT_TO_TREE_SITTER_LANGUAGE,
)

# Third party
from tree_sitter import Language, Parser, Tree, Node
from tree_sitter_languages import get_parser, get_language
import rustworkx as rx
import igraph as ig
import leidenalg as la
import numpy as np
from tqdm import tqdm

NODE_TYPE_LITERAL = Literal["definition", "reference"]
BACKTRACK_LIMIT = 2

# Helpers


def batch_list(lst: list, batch_size: int = 10000):
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]


class ASTNode:
    def __init__(
        self,
        id: int,
        path: str,
        node_type: str,
        variant: TreeSitterNodeVariant,
        node_key: str | None = None,
        name_node: Node = None,
        body_node: Node = None,
    ):
        self.id = id
        self.path = path
        self.ext = os.path.splitext(path)[1]
        self.language = EXT_TO_TREE_SITTER_LANGUAGE.get(self.ext)
        self.name: str = None
        self.node_type: NODE_TYPE_LITERAL = node_type
        self.node_key: str = node_key
        self.variant: TreeSitterNodeVariant | None = variant
        self.name_range: Range = None
        self.code_range: Range = None
        self.error = None
        self.callers: List[int] = []
        self.calling: List[int] = []
        self.ambiguous_reference: bool = False
        if name_node or body_node:
            self.from_treesitter_nodes(name_node, body_node)

    def from_treesitter_nodes(self, name_node: Node, body_node: Node):
        "Uses treesitter nodes to populate the name, name_range, and code_range properties of an ASTNode."
        if name_node:
            self.name = name_node.text.decode("utf-8")
            start_line, start_col = name_node.start_point
            end_line, end_col = name_node.end_point
            self.name_range = Range(
                start_line,
                start_col,
                end_line,
                end_col,
            )
            self.code_range = Range(
                start_line,
                start_col,
                end_line,
                end_col,
            )
        if body_node:
            body_start_line, body_start_col = body_node.start_point
            body_end_line, body_end_col = body_node.end_point
            self.code_range = Range(
                body_start_line,
                body_start_col,
                body_end_line,
                body_end_col,
            )

    def __repr__(self):
        return f"ASTNode(path={self.path}, name={self.name}, name_range={str(self.name_range)}, code_range={str(self.code_range)}, type={self.node_type}, callers={len(self.callers)}, calling={len(self.calling)})"

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.path, self.name, self.name_range, self.code_range))

    def __eq__(self, other):
        return (
            self.path == other.path
            and self.name == other.name
            and self.name_range == other.name_range
            and self.code_range == other.code_range
            and self.node_type == other.node_type
        )

    def to_dict(self):
        """
        Serializes the ast node into a dict of id, path, name, name_range, code_range.
        Note that the name_range, and code_range are serialized into 4-tuples of ints, with the structure being (start_line, start_column, end_line, end_column).
        """
        return {
            "id": self.id,
            "path": self.path,
            "name": self.name,
            "name_range": self.name_range.to_list(),
            "code_range": self.code_range.to_list(),
            # "type": self.node_type,
        }

    def invalid(self):
        "Returns True if a node doesn't have a name and is missing either a name_range or a code_range."
        return all([not self.name, not self.name_range or not self.code_range])

    @classmethod
    def from_dict(cls, ast_node_dict: Dict):
        """
        Converts a serialized ASTNode (usually from a Graph/Relational DB) back into a ASTNode Object.
        Do note that the ast_node_dict requires and id, path, name, and 4-tuples name_range and code_range.
        The structure of both 4-tuples is (start_line, start_column, end_line, end_column), and each tuple member is an int
        """
        ast_node = cls(
            id=ast_node_dict["id"],
            path=ast_node_dict["path"],
            node_type="definition",
            variant=TreeSitterNodeVariant.CALLABLE,
        )
        ast_node.name = ast_node_dict["name"]
        ast_node.name_range = Range(
            start_line=ast_node_dict["name_range"][0],
            start_column=ast_node_dict["name_range"][1],
            end_line=ast_node_dict["name_range"][2],
            end_column=ast_node_dict["name_range"][3],
        )
        ast_node.code_range = Range(
            start_line=ast_node_dict["code_range"][0],
            start_column=ast_node_dict["code_range"][1],
            end_line=ast_node_dict["code_range"][2],
            end_column=ast_node_dict["code_range"][3],
        )
        return ast_node


class ScopeASTBuilder:
    def __init__(self, files: List[File], timeit: bool = False):
        self.files = files
        self.ext_set = set(file.file_extension for file in files)
        self.ext_to_sitter_language: Dict[str, Language] = {}
        self.ext_to_parser: Dict[str, Parser] = {}
        self.trees: Dict[str, Tree] = {}
        self.nodes: Dict[str, List[ASTNode]] = {}
        self.node_lookup: Dict[int, ASTNode] = {}
        self.language_groups: Dict[str, Set[str]] = defaultdict(set)
        self.global_id = 0
        self.timeit = timeit
        self._setup_parsers()
        self._setup_trees(timeit)
        self._parse()

    @property
    def has_errors(self) -> bool:
        "Unused, but checks if any of the nodes have a Truth-y value for node.error."
        return any(node.error for node in self.nodes.values())

    def _setup_parsers(self):
        "Sets up all treesitter language parsers ahead of time, for performance reasons."
        for ext in self.ext_set:
            lang = EXT_TO_TREE_SITTER_LANGUAGE.get(ext)
            if lang is None:
                continue
            parser_language = get_language(lang)
            self.ext_to_sitter_language[ext] = parser_language
            parser = get_parser(lang)
            self.ext_to_parser[ext] = parser

    def _setup_trees(self, timeit):
        "Runs treesitter to parse source code for each file, creating Tree objects and storing them under self.trees"
        time_start = time.time()
        files_to_remove = set()
        for file in self.files:
            parser = self.ext_to_parser.get(file.file_extension)
            if parser is None:
                files_to_remove.add(file.abs_path)
                continue
            file_content = file.content.encode()
            self.trees[file.path] = parser.parse(file_content)
        _files = [file for file in self.files if file.abs_path not in files_to_remove]
        self.files = _files
        if self.timeit:
            print(f"Time taken to setup trees: {time.time() - time_start} seconds")

    def _walk_tree(self, tree: Tree, node_types: Set[str]):
        "Used by walk_trees() function to traverse a TreeSitter tree for a particular file and extract matching node types"
        cursor = tree.walk()
        decode_text = lambda x: x.text.decode("utf-8")
        stack = []

        while True:
            if cursor.node.type in node_types:
                yield {
                    "type": cursor.node.type,
                    "text": decode_text(cursor.node),
                    "name": decode_text(cursor.node.child_by_field_name("identifier")),
                    "start_point": cursor.node.start_point,
                    "end_point": cursor.node.end_point,
                }

            # If has children, tell the stack to process them
            if cursor.goto_first_child():
                stack.append(True)
                continue

            # No children, try to go to next sibling
            while True:
                if cursor.goto_next_sibling():
                    break
                if not stack:
                    return
                stack.pop()
                cursor.goto_parent()

    def walk_trees(self):
        """Prototype function. Currently unused by lets you traverse raw AST without needing to write custom queries."""
        tree_data = defaultdict(list)
        test_node_types_python = ["function_definition", "class_definition"]
        # test_node_types = {"call"}
        for file_name, tree in self.trees.items():
            for node in self._walk_tree(tree, test_node_types_python):
                tree_data[file_name].append(node)
        return dict(tree_data)

    def _parse_file(self, file: RepoFile) -> List[ASTNode]:
        """Parse a file using Tree-sitter to extract AST nodes for definitions and references.

        This method processes a single file to identify code elements (like functions, classes, etc.)
        by applying language-specific Tree-sitter queries. It handles both definitions and references
        of code elements, creating ASTNode objects for each match.

        Args:
            file (RepoFile): The file to parse, containing the file path and extension information.

        Returns:
            List[ASTNode]: A list of ASTNode objects representing the definitions and references
            found in the file. Each node contains information about its location, type, and
            associated code ranges.

        Note:
            - If the file's language is not supported or the tree is not available, returns an empty list
            - Handles errors gracefully by skipping problematic queries or matches
            - Each ASTNode is assigned a unique global ID
            - Invalid nodes (missing name or ranges) are skipped
        """
        
        tree = self.trees.get(file.path)
        parser_language = self.ext_to_sitter_language.get(file.file_extension)
        lang = EXT_TO_TREE_SITTER_LANGUAGE.get(file.file_extension)
        if not lang or not tree:
            return []
        query_groups = TREE_SITTER_REF_DEF_QUERIES.get(lang, {})

        nodes = set()
        for ident_type, queries in query_groups.items():
            for query in queries:
                ref_query = queries[query]["query"]
                output_name = queries[query]["output_name"]
                output_body = queries[query].get("output_body")
                variant = queries[query].get("variant")
                try:
                    sitter_query = parser_language.query(ref_query)
                except Exception as e:
                    print(
                        f"Error parsing query {ref_query} for file {file.file_name}: {e}"
                    )
                    continue
                try:
                    matches = sitter_query.matches(tree.root_node)
                except Exception as e:
                    print(
                        f"Error matching query {ref_query} for file {file.file_name}: {e}"
                    )
                    continue

                # Each match is a tuple of (match_index, match_dict, which can have multiple keys)
                # TODO: We only have single queries w/ multiple keys, we need to support multiple keys
                for match in matches:
                    try:
                        ts_node = match[1]
                        if not ts_node:
                            continue
                        ts_name_node = ts_node.get(output_name)
                        ts_body_node = ts_node.get(output_body)
                        node_key = query
                        node = ASTNode(
                            self.global_id,
                            file.path,
                            ident_type,
                            variant,
                            node_key,
                            ts_name_node,
                            ts_body_node,
                        )
                        self.global_id += 1
                        if node.invalid():
                            print(f"Skipping invalid ASTNode: {node}")
                            continue
                        nodes.add(node)
                    except Exception as e:
                        import traceback

                        traceback.print_exc()
                        print(
                            f"Error constructing ASTNode for query {ref_query} for file {file.file_name}: {e}"
                        )
        return list(nodes)

    def _parse(self):
        if self.timeit:
            files = tqdm(self.files, total=len(self.files), desc="Parsing files")
        else:
            files = self.files
        for file in files:
            self.nodes[file.path] = self._parse_file(file)
            self.language_groups[file.language].add(file.path)
        for nodes in self.nodes.values():
            for node in nodes:
                self.node_lookup[node.id] = node

    def mark_ambiguous_references(self):
        """
        Deprecated for now due to scope (no pun intended) of ScopeASTBuilder changing. 
        Originally used for marking references as ambiguous if there are multiple definitions with the same name as the reference being checked.
        """
        shared_definitions = defaultdict(list)
        for d in self.definitions():
            shared_definitions[d.name].append(d)
        shared_definitions = {k: v for k, v in shared_definitions.items() if len(v) > 1}
        for r in self.references():
            if r.name in shared_definitions:
                shared_defs = shared_definitions[r.name]
                ref_and_def_share_location = any(r.path == d.path for d in shared_defs)
                if not ref_and_def_share_location:
                    r.ambiguous_reference = True


class ScopeAST:
    def __init__(self, files: List[File], build: bool = True, timeit: bool = False):
        self.files: List[File] = None
        self.file_lookup: Dict[str, File] = None
        self.nodes: Dict[str, List[ASTNode]] = None
        self.defn_nodes_by_name: Dict[str, List[ASTNode]] = None
        self.language_groups: Dict[str, Set[str]] = None
        if build:
            builder = ScopeASTBuilder(files, timeit)
            self.files = builder.files
            self.file_lookup = {f.path: f for f in self.files}
            self.nodes = builder.nodes
            self.defn_nodes_by_name = defaultdict(list)
            for nodes in self.nodes.values():
                for node in nodes:
                    if node.node_type == "definition":
                        self.defn_nodes_by_name[node.name].append(node)
            self.language_groups = builder.language_groups

    def __repr__(self):
        unique_definitions = {d.name for d in self.definitions()}
        unique_references = {r.name for r in self.references()}
        len_defs = len(self.definitions())
        len_refs = len(self.references())
        len_defs_unique = len(unique_definitions)
        len_refs_unique = len(unique_references)
        return f"ScopeAST(files={len(self.files)} defs={len_defs} unique_defs={len_defs_unique} refs={len_refs} unique_refs={len_refs_unique})"

    @classmethod
    def empty(cls):
        "Necessary for the split_by_language function to work."
        return cls([])

    def split_by_language(self) -> List["ScopeAST"]:
        "Not Used Currently. But breaks up a single ScopeAST into multiple ScopeAST, all language specific."
        asts = []
        for lang, paths in self.language_groups.items():
            files = [f for f in self.files if f.path in paths]
            nodes = defaultdict(list)
            for path, node_list in self.nodes.items():
                if path in paths:
                    nodes[lang].extend(node_list)
            ast = ScopeAST.empty()
            ast.files = files
            ast.nodes = nodes
            ast.language_groups = {lang: paths}
            asts.append(ast)
        return asts

    @cache
    def definitions_by_name(self, name) -> List[ASTNode]:
        """Gets definitions by a specific name e.g foobar()."""
        return self.defn_nodes_by_name.get(name, [])

    @cache
    def definitions(self, path: str = None) -> List[ASTNode]:
        "Gets all nodes marked as definitions in the ScopeAST. Path optional."
        search_callback = lambda p, node: node.node_type == "definition"
        return self.search(search_callback, path)

    @cache
    def references(self, path: str = None) -> List[ASTNode]:
        "Gets all nodes marked as references in ScopeAST. Path optional."
        search_callback = lambda p, node: node.node_type == "reference"
        return self.search(search_callback, path)

    def search(
        self, search_callback: Callable[[RepoFile, ASTNode], bool], path: str = None
    ) -> List[ASTNode]:
        "Flexible 'search engine' for ASTNode based on a callback that takes a RepoFile and ASTNode as args and returns a bool. True indicates inclusion in the search results. You can optionally include a path. If a path is included, the callback will be ignored. This is for performance reasons."
        hits = []
        if path:
            _nodes = self.nodes[path]
            file = self.file_lookup[path]
            for node in _nodes:
                if search_callback(file, node):
                    hits.append(node)
        else:
            for file in self.files:
                for node in self.nodes[file.path]:
                    if search_callback(file, node):
                        hits.append(node)
        return hits


class ApproximateCallGraphBuilder:
    def __init__(
        self, ast: ScopeAST, timeit: bool = False, prune_references: bool = True
    ):
        self.ast = ast
        self.callgraph_lookup: Dict[int, ASTNode] = {}
        self.callgraph: rx.PyDiGraph = rx.PyDiGraph(multigraph=False)
        self.node_indices: Dict[int, int] = {}
        self.timeit = timeit
        self.prune_references = prune_references

    @cache
    def get_containing_def_for_ref(self, path: str, ref_range: Range) -> ASTNode | None:
        "For a given Ref's range (e.g start/end lines) + path, find it's calling definition, e.g the definition that contains it."
        containing_defs: List[ASTNode] = []
        for defn in self.ast.definitions(path):
            if defn.code_range.contains(ref_range):
                containing_defs.append(defn)
        if not containing_defs:
            return None
        return min(containing_defs, key=lambda x: x.code_range.height())

    @cache
    def backtrack_ref_to_origin_defs(self, ref: ASTNode) -> List[int]:
        """
        For a given Ref, search all Definitions that match it by name, path, and language.
        If an exact match is not found, then this function will return more than one node ids.
        In this case, a ref will have multiple, necessarily ambiguous definitions.
        We apply a hard BACKTRACK_LIMIT to truncate the space of possible ambiguous references.
        """
        # Step 1: Look inside the same file.
        for defn in self.ast.definitions(ref.path):
            if defn.name == ref.name and defn.language == ref.language:
                return [defn.id]

        # Step 2: Look at different files
        found_origin_defs_ids = []
        for defn in self.ast.definitions_by_name(ref.name):
            if defn.path == ref.path:
                continue
            if defn.language == ref.language:
                found_origin_defs_ids.append(defn.id)

        return list(set(found_origin_defs_ids))[:BACKTRACK_LIMIT]

    def prune_refs(self):
        """
        Removes references via basic heuristics (slightly biased).
        If Defn's pointed to by defn.calling are ambiguous and have the same name, prefer the ones that shares the same path with the Defn.
        """
        for defn_id in self.callgraph_lookup.keys():
            defn = self.callgraph_lookup[defn_id]

            # Prune the calling list
            calling_ids_keep = []
            for calling_id in defn.calling:
                calling_defn = self.callgraph_lookup[calling_id]
                if calling_defn.name == defn.name and calling_defn.path == defn.path:
                    continue
                calling_ids_keep.append(calling_id)
            self.callgraph_lookup[defn_id].calling = calling_ids_keep

            # Prune the callers list
            callers_ids_keep = []
            for caller_id in defn.callers:
                caller_defn = self.callgraph_lookup[caller_id]
                if caller_defn.name == defn.name and caller_defn.path == defn.path:
                    continue
                callers_ids_keep.append(caller_id)
            self.callgraph_lookup[defn_id].callers = callers_ids_keep

    def _mark_refs_for_path(self, path : str):
        "Gets the definitions for each reference in a particular path."
        # Iterate over all references in the path, and track down their definition
        for r in self.ast.references(path):
            containing_defn = self.get_containing_def_for_ref(path, r.name_range)
            if not containing_defn:
                continue
            origin_defs_ids = self.backtrack_ref_to_origin_defs(r)
            self.callgraph_lookup[containing_defn.id].calling.extend(origin_defs_ids)
            for origin_def_id in origin_defs_ids:
                self.callgraph_lookup[origin_def_id].callers.append(containing_defn.id)

    def _mark_references(self, progress_bar: bool = False):
        time_start = time.time()
        paths = list(set([d.path for d in self.ast.definitions()]))
        if progress_bar:
            paths = tqdm(paths, total=len(paths), desc="Marking references")
        for path in paths:
            self._mark_refs_for_path(path)
        self.prune_refs()
        if self.timeit:
            print(f"Time taken to mark references: {time.time() - time_start} seconds")

    def _remove_cycles(self):
        """
        Removes all the cycles in our approximate CG. This is necessary for network analysis, as most only support DAGs.
        Keep in mind it may not be entirely accurate in preserving the true structure of a codebase.
        """
        while not rx.is_directed_acyclic_graph(self.callgraph):
            cycles = rx.digraph_find_cycle(self.callgraph)
            for cycle in cycles:
                source, target = cycle
                print(f"Breaking cycle at {source} -> {target}")
                self.callgraph.remove_edge(source, target)
                break

    def run(self, progress_bar: bool = False):
        """
        Turns the ScopeAST object into an RustWorkX DiGraph object.
        1. It marks each ASTNode with constructs that call it and/or are called by it (via the calling/caller properties). This is done via the _mark_references function.
        2. We add nodes and edges to the DiGraph. The edge inserts are batched to support extremely large codebases.
        3. After the DiGraph is constructed, we remove all cycles from the callgraph.
        """
        # self.ast.mark_ambiguous_references()
        self.callgraph_lookup = {d.id: d for d in self.ast.definitions()}
        self._mark_references(progress_bar)
        time_start = time.time()

        nodes_added = self.callgraph.add_nodes_from(self.ast.definitions())
        print(f"Adding {len(self.ast.definitions())} nodes to the graph")

        definitions = list(self.callgraph_lookup.values())
        self.node_indices = {d.id: ni for ni, d in zip(nodes_added, definitions)}
        defn_batches = batch_list(definitions)

        if progress_bar:
            defn_batches = tqdm(
                defn_batches,
                total=(len(list(definitions)) // 10000),
                desc="Formatting edges",
            )

        num_refs = 0
        for defn_batch in defn_batches:
            edges_to_add = []
            for d in defn_batch:
                for caller in d.callers:
                    caller_id = self.node_indices[caller]
                    d_id = self.node_indices[d.id]
                    num_refs += 1
                    edges_to_add.append((caller_id, d_id, [caller_id, d_id]))
                for callee in d.calling:
                    callee_id = self.node_indices[callee]
                    d_id = self.node_indices[d.id]
                    num_refs += 1
                    edges_to_add.append((d_id, callee_id, [d_id, callee_id]))
            self.callgraph.add_edges_from(edges_to_add)

        print(f"Added {num_refs} edges to the callgraph")
        self._remove_cycles()

        if self.timeit:
            print(
                f"Time taken to build callgraph with rustworkx: {time.time() - time_start} seconds"
            )


class ApproximateCallGraph:
    def __init__(
        self,
        callgraph: rx.PyDiGraph,
        callgraph_lookup: Dict[int, ASTNode],
        node_indices: Dict[int, int],
    ):
        self.callgraph = callgraph
        self.callgraph_lookup = callgraph_lookup
        self.node_indices = node_indices
        self.reversed_node_indices = {v: k for k, v in node_indices.items()}

    def __repr__(self):
        return f"ApproximateCallGraph(nodes={len(self.callgraph.nodes())}, edges={len(self.callgraph.edges())})"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def build(
        cls,
        ast: ScopeAST,
        timeit: bool = False,
        progress_bar: bool = False,
        prune_references: bool = True,
    ):  
        "Constructs the ApproximateCallgraph object by passing the AST into the ApproximateCallGraphBuilder factory class."
        builder = ApproximateCallGraphBuilder(ast, timeit, prune_references)
        builder.run(progress_bar)
        return cls(
            callgraph=builder.callgraph,
            callgraph_lookup=builder.callgraph_lookup,
            node_indices=builder.node_indices,
        )

    @classmethod
    def from_nodes_and_edges(cls, nodes: List[ASTNode], edges: List[Tuple[int, int]]):
        """
        Helper function primarily used in testing the library.
        However, it can also be used to reconstruct the ApproximateCallgraph object if your nodes and edges are stored elsewhere, like Postgres.
        Keep in mind, if you are reconstructing ASTNodes from a serialized form, use the ASTNode.from_dict() classmethod.
        """
        callgraph = rx.PyDiGraph(multigraph=False)
        callgraph.add_nodes_from(nodes)
        callgraph.add_edges_from([(s, t, [s, t]) for s, t in edges])
        return cls(
            callgraph=callgraph,
            callgraph_lookup={d.id: d for d in nodes},
            node_indices={d.id: i for i, d in enumerate(nodes)},
        )

    @cached_property
    def nodes(self) -> List[ASTNode]:
        "All of the nodes in the callgraph."
        return self.callgraph.nodes()

    @cached_property
    def edges(self) -> List[Tuple[int, int]]:
        """
        Gets all the edges in the callgraph. Each edge is a 2-tuple of ints e.g (int, int).
        The first value is the source node id, the second value is the target node id.
        """
        return self.callgraph.edges()

    @cached_property
    def files(self) -> List[str]:
        "Gets all all the unique relative file paths in the callgraph."
        return list(set([d.path for d in self.nodes]))

    @cached_property
    def identifiers(self) -> List[str]:
        "All of the unique node names in the callgraph. This could be the name of a function, class, etc."
        return list({d.name for d in self.nodes})

    def to_igraph(self, directed: bool = True) -> ig.Graph:
        """
        Converts our RustworkX graph into a igraph Graph. 
        This is required for clustering the graph into communities, and for other network analysis purposes, if you so choose.
        This function is used in the indexing_queue function.
        """
        edges = []
        for node in self.nodes:
            for caller in self.callers(node):
                edges.append({"source": node.id, "target": caller.id})
        nodes = [{"name": node.id} for node in self.nodes]
        graph = ig.Graph.DictList(
            vertices=nodes,
            edges=edges,
            directed=directed,
            edge_foreign_keys=["source", "target"],
        )
        return graph

    def is_acyclic(self) -> bool:
        "Deprecated. We always break cycles when we construct the ApproximateCallgraph."
        return rx.is_directed_acyclic_graph(self.callgraph)

    def adjacency_matrix(self) -> np.ndarray:
        "Deprecated. But a useful wrapper function that calls RustworkX's adjacency matrix func."
        return rx.adjacency_matrix(self.callgraph)

    def callers(self, node: ASTNode) -> List[ASTNode]:
        "Get all the ASTNodes that call `node`."
        id = self.node_indices[node.id]
        return self.callgraph.predecessors(id)

    def calling(self, node: ASTNode) -> List[ASTNode]:
        "Get all the ASTNodes that are called by `node`."
        id = self.node_indices[node.id]
        return self.callgraph.successors(id)

    def longest_path(self):
        "Gets the longest directed path in the callgraph."
        path_indices = rx.dag_longest_path(self.callgraph)
        node_indices = [self.reversed_node_indices[i] for i in path_indices]
        nodes = [self.callgraph_lookup[i] for i in node_indices]
        return nodes

    def indexing_queue(self, max_community_size=0) -> List[Tuple[int, ASTNode]]:
        """ 
        Prototype function that turns an ApproximateCallgraph into a Queue of type ASTNode.
        This behavior only makes sense in the context of JIT Indexing, whereby you have a very large repo with certain latency constraints,
        and you want to index certain nodes first, so that users can start using Q&A or other AI features as fast as possible without the entire repo being indexed.
        This is an obvious tradeoff, but again - it makes sense if your users care about latency over accuracy.
        
        We do a ModularityVertexPartition with the leidenalg package, which uses the Leiden Algorithm, which itself is an extension of the Louvain algorithm.
        Leiden is better suited for graphs that have hierarchical communities, e.g communities inside communinities. This makes it a perfect fit for codebases.
        """
        longest_path_len = len(self.longest_path())
        num_nodes = len(self.nodes)

        # max_community_size = 0 # min(num_nodes // 10, longest_path_len * 5)
        ig_graph = self.to_igraph()
        partition = la.find_partition(
            ig_graph, la.ModularityVertexPartition, max_comm_size=max_community_size
        )
        subgraphs: List[ig.Graph] = [sg for sg in partition.subgraphs()]
        subgraphs = sorted(subgraphs, key=lambda x: x.vcount(), reverse=True)
        max_subgraph_size = subgraphs[0].vcount()

        seen_nodes = set()
        ordered_nodes: List[Tuple[int, ASTNode]] = []
        low_priority_nodes: List[Tuple[int, ASTNode]] = []
        for rank, subgraph in enumerate(subgraphs):
            num_vertices = subgraph.vcount()
            for vertex in subgraph.vs:
                vertex_id = int(vertex["name"])
                node = self.callgraph_lookup[vertex_id]
                if node.id not in seen_nodes:
                    if num_vertices > 1 and (node.calling or node.callers):
                        ordered_nodes.append((rank, node))
                    else:
                        low_priority_nodes.append((-1, node))
                    seen_nodes.add(node.id)

        ordered_nodes.extend(low_priority_nodes)
        return ordered_nodes

        # print(f"Ordered file paths (first 1000): {ordered_file_paths[:1000]}")
        # print()
        # print(f"Low priority files (first 1000): {low_priority_files[:1000]}")
        # print()

        # # print(f"Max community size: {max_community_size}")
        # print(f"Actual max subgraph size: {max_subgraph_size}")
        # print(f"Number of subgraphs: {len(subgraphs)}")
        # print(f"Number of ordered nodes: {len(ordered_nodes)}")
        # print(f"Number of nodes in callgraph: {len(self.nodes)}")
        # print(f"Number of low priority nodes: {len(low_priority_nodes)}")
        # print(f"Number of files in callgraph: {len(self.files)}")
