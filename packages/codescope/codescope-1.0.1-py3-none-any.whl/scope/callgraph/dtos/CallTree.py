from typing import List, Callable
from scope.callgraph.dtos.Definition import Definition
from scope.callgraph.enums.CallTreeType import CallTreeType
from scope.callgraph.dtos.CallStack import CallStack


class CallTree(object):
    def __init__(
        self,
        root_defn: Definition,
        all_defns: List[Definition],
        direction: CallTreeType,
        depth=-1,
    ):
        """Initialize a CallTree object.

        Args:
            root_defn (Definition): The root definition from which to build the call tree
            all_defns (List[Definition]): List of all definitions available in the codebase
            direction (CallTreeType): Direction of the call tree (UP for callers, DOWN for callees)
            depth (int, optional): Maximum depth of the call tree. Defaults to -1 (unlimited).
        """
        self.root_defn = root_defn
        self.direction = direction
        self.depth = depth
        self.tree = self._build(all_defns)

    def __len__(self) -> int:
        """Return the number of call stacks in the tree.

        Returns:
            int: Number of call stacks
        """
        return len(self.tree)

    def __iter__(self):
        """Return an iterator over the call stacks in the tree.

        Returns:
            Iterator[CallStack]: Iterator over call stacks
        """
        return iter(self.tree)

    def __getitem__(self, index: int) -> CallStack:
        """Get a call stack at the specified index.

        Args:
            index (int): Index of the call stack to retrieve

        Returns:
            CallStack: The call stack at the specified index
        """
        return self.tree[index]

    def _build(self, all_defns: List[Definition]) -> List[CallStack]:
        """Build the call tree using iterative depth-first search.

        Args:
            all_defns (List[Definition]): List of all definitions available in the codebase

        Returns:
            List[CallStack]: List of call stacks representing the call tree
        """
        corpus = {d.id: d for d in all_defns}

        def iterative_dfs(start_ref):
            stack = [(start_ref, [start_ref], set())]
            all_paths = []

            while stack:
                current_ref, current_path, seen = stack.pop()
                if self.depth != -1 and len(current_path) > self.depth:
                    all_paths.append(current_path)
                    continue

                if self.direction == CallTreeType.UP:
                    new_refs = corpus[current_ref.id].referenced_by
                else:
                    new_refs = corpus[current_ref.id].referencing

                unseen_refs = [ref for ref in new_refs if ref.id not in seen]
                if not unseen_refs:
                    all_paths.append(current_path)
                else:
                    for new_ref in unseen_refs:
                        new_seen = seen.copy()
                        new_seen.add(new_ref.id)
                        stack.append((new_ref, current_path + [new_ref], new_seen))

            return all_paths

        if self.direction == CallTreeType.UP:
            initial_refs = self.root_defn.referenced_by
        else:
            initial_refs = self.root_defn.referencing

        all_paths = []
        for ref in initial_refs:
            all_paths.extend(iterative_dfs(ref))

        # Convert references to definitions, then wrap in CallStack
        stacks = [[corpus[ref.id] for ref in path] for path in all_paths]
        return [CallStack(stack, self.direction) for stack in stacks]

    def find(
        self,
        root_cb: Callable[[str, Definition], bool] = lambda x, y: True,
        tail_cb: Callable[[str, Definition], bool] = lambda x, y: True,
    ) -> List[CallStack]:
        """Find call stacks that match the given criteria.

        Args:
            root_cb (Callable[[str, Definition], bool], optional): Callback function to filter root definitions.
                Takes path and definition as arguments. Defaults to lambda x, y: True.
            tail_cb (Callable[[str, Definition], bool], optional): Callback function to filter tail definitions.
                Takes path and definition as arguments. Defaults to lambda x, y: True.

        Returns:
            List[CallStack]: List of call stacks that match the criteria
        """
        matching_stacks = []
        for stack in self.tree:
            if root_cb(stack.root_defn.path, stack.root_defn) and tail_cb(
                stack.root_defn.path, stack.root_defn
            ):
                matching_stacks.append(stack)
        return matching_stacks

    def leafs(self):
        """Get all leaf definitions in the call tree.

        Returns:
            List[Definition]: List of leaf definitions
        """
        return [stack.tail() for stack in self.tree]

    def roots(self):
        """Get all root definitions in the call tree.

        Returns:
            List[Definition]: List of root definitions
        """
        return [stack.root() for stack in self.tree]
