import enum


class TreeSitterNodeVariant(enum.Enum):
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    MODULE = "module"
    STRUCT = "struct"
    CALLABLE = "callable"
