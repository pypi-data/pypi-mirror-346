# Standard library
from dataclasses import dataclass

# Local
from scope.callgraph.dtos.Range import Range
from scope.callgraph.utils import stable_hash

# from scope.dtos.Definition import Definition
from scope.callgraph.enums import ReferenceType


@dataclass
class ReferenceLSP(object):
    id: str
    name: str
    type: str
    path: str
    language: str
    range: Range
    snippet_range: Range
    reference_range: Range


@dataclass
class ReferenceSerde(object):
    id: str
    name: str
    type: str
    path: str
    language: str
    range: Range
    snippet_range: Range
    reference_range: Range


class Reference(object):
    def __init__(self, ref: ReferenceLSP | ReferenceSerde, **kwargs):
        """Initialize a Reference object from either a ReferenceLSP or ReferenceSerde object.

        Args:
            ref (ReferenceLSP | ReferenceSerde): The reference data object containing all necessary fields
            **kwargs: Additional keyword arguments (currently unused)
        """
        self.id = ref.id
        self.name = ref.name
        self.type = ref.type
        self.path = ref.path  # File with the containing definition
        self.language = ref.language
        # Identifier range (i.e. `def foo():\n\treturn "bar"` -> range of `def foo():`)
        self.range = ref.range
        # Full range of containing definition (i.e. range of `def foo():\n\tcall_bar()`)
        self.snippet_range = ref.snippet_range
        # Reference range (i.e. `def foo():\n\tcall_bar()` -> range of `call_bar()`)
        self.reference_range = ref.reference_range

        # NOTE: path, range, snippet_range are all attributes of the containing definition

    def __hash__(self):
        """Generate a hash value for the Reference object based on name, path, and range.

        Returns:
            int: A hash value for the Reference object
        """
        return stable_hash(
            {"name": self.name, "path": self.path, "range": self.range.to_dict()},
            as_int=True,
        )

    def __eq__(self, other):
        """Compare this Reference object with another for equality.

        Args:
            other: The object to compare with

        Returns:
            bool: True if the objects are equal, False otherwise
        """
        if not isinstance(other, Reference):
            return NotImplemented

        return self.path == other.path and self.range == other.range

    def __str__(self) -> str:
        """Return a string representation of the Reference object.

        Returns:
            str: A string containing the name, path, range, and reference range
        """
        return f"Reference(name={self.name} path={self.path}, range={self.range}, ref_range={self.reference_range})"

    def to_dict(self):
        """Convert the Reference object to a dictionary representation.

        Returns:
            dict: A dictionary containing all the Reference object's attributes
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "path": self.path,
            "language": self.language,
            "range": self.range.to_dict(),
            "snippet_range": self.snippet_range.to_dict(),
            "reference_range": self.reference_range.to_dict(),
        }

    # def get_containing_def(self, defs: List[Definition]):
    #     pass

    # def get_containing_ref(self, refs: List["Reference"]):
    #     pass

    @classmethod
    def undirected(cls, path: str, reference_range: Range):
        """Create an undirected Reference object with minimal information.

        Args:
            path (str): The file path
            reference_range (Range): The range of the reference

        Returns:
            Reference | None: A new Reference object or None if creation fails
        """
        try:
            ref = ReferenceLSP(
                id=None,
                name=None,
                type=None,
                path=path,
                language=None,
                range=None,
                snippet_range=None,
                reference_range=reference_range,
            )
        except Exception as e:
            print(f"Reference::undirected ERROR: {e}")
            return None
        return cls(ref)

    @classmethod
    # TODO: figure out how to get typehint for defn to map to Definition. Circular import issue
    def from_def(cls, defn: object, partial_ref: "Reference", ref_type: ReferenceType):
        """Create a Reference object from a definition and partial reference.

        Args:
            defn (object): The definition object to create the reference from
            partial_ref (Reference): A partial reference containing the reference range
            ref_type (ReferenceType): The type of reference to create

        Returns:
            Reference | None: A new Reference object or None if creation fails
        """
        try:
            ref = ReferenceLSP(
                id=defn.id,
                name=defn.name,
                type=ref_type.value,
                path=defn.path,
                language=defn.language,
                range=defn.range,
                snippet_range=defn.snippet_range,
                reference_range=partial_ref.reference_range,
            )
        except Exception:
            return None
        return cls(ref)

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Reference object from a dictionary.

        Args:
            data (dict): A dictionary containing the reference data

        Returns:
            Reference: A new Reference object created from the dictionary data
        """
        ref = ReferenceSerde(
            id=data.get("id"),
            name=data.get("name"),
            type=data.get("type"),
            path=data.get("path"),
            language=data.get("language"),
            range=Range(**data.get("range")),
            snippet_range=Range(**data.get("snippet_range")),
            reference_range=Range(**data.get("reference_range")),
        )
        return cls(ref)
