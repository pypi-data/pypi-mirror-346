from typing import List
from scope.callgraph.dtos.Definition import Definition
from scope.callgraph.enums import CallTreeType


class CallStack(object):
    """A class representing a call stack of function definitions with a specific direction.
    
    A call stack represents a sequence of function definitions that form a call chain,
    either in the forward (callee) or backward (caller) direction.
    """

    def __init__(self, stack: List[Definition], direction: CallTreeType):
        """Initialize a new CallStack instance.
        
        Args:
            stack: A list of Definition objects representing the call chain
            direction: The direction of the call tree (CallTreeType enum)
        """
        self.stack = stack
        self.direction = direction

    def __str__(self) -> str:
        """Return a string representation of the call stack.
        
        Returns:
            A formatted string showing the call stack with indentation and root information
        """
        stack_str = []
        indent_width = 0
        for defn in self.stack:
            stack_str.append(f"{indent_width * ' '}> {defn.pprint()}")
            indent_width += 2
        trace = "\n".join(stack_str)
        root_defn = self.root()
        return f"CallStack(name={root_defn.name}, path={root_defn.path}, direction={self.direction}, id={root_defn.id}):\n{trace}\n"

    def __len__(self) -> int:
        """Return the number of definitions in the call stack.
        
        Returns:
            The length of the stack
        """
        return len(self.stack)

    def slice(self, start: int, end: int) -> "CallStack":
        """Create a new CallStack containing a subset of the definitions.
        
        Args:
            start: The starting index (inclusive)
            end: The ending index (exclusive)
            
        Returns:
            A new CallStack instance containing the sliced definitions
            
        Raises:
            ValueError: If start or end indices are out of bounds
        """
        if start < 0 or end > len(self.stack):
            raise ValueError(f"Invalid slice: start={start}, end={end}")
        return CallStack(self.stack[start:end])

    def root(self) -> Definition:
        """Get the root definition of the call stack.
        
        Returns:
            The first Definition in the stack
        """
        return self.stack[0]

    def tail(self) -> Definition:
        """Get the tail definition of the call stack.
        
        Returns:
            The last Definition in the stack
        """
        return self.stack[-1]
