from scope.callgraph.enums.TreeSitterNodeVariant import TreeSitterNodeVariant

EXT_TO_TREE_SITTER_LANGUAGE = {
    ".js": "tsx",
    ".jsx": "tsx",
    ".ts": "tsx",
    ".tsx": "tsx",
    ".mjs": "tsx",
    ".py": "python",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "cpp",
    ".h": "cpp",
    ".hpp": "cpp",
    ".cs": "cpp",
    ".rb": "ruby",
    # ".md": "markdown",
    # ".rst": "markdown",
    # ".txt": "markdown",
    # ".erb": "embedded-template",
    # ".ejs": "embedded-template",
    # ".html": "embedded-template",
    ".erb": "html",
    ".ejs": "html",
    ".html": "html",
    ".vue": "html",
    ".php": "php",
}

TREE_SITTER_REF_DEF_QUERIES = {
    "python": {
        "definition": {
            "function_definition": {
                "query": """
                    (function_definition 
                        name: (identifier) @definition_name
                    ) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "class_definition": {
                "query": """
                    (class_definition
                        name: (identifier) @definition_name
                    ) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
        },
        "reference": {
            # handles things like `func()`
            "call_reference": {
                "query": """
                    (call function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            # handles things like `obj.method()`
            "call_dot_reference": {
                "query": """
                    (call 
                        function: (attribute 
                            attribute: (identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
            # TODO: handles things like `obj.method`
        },
    },
    # This covers JS and TS
    "tsx": {
        "definition": {
            # example: function oldStyleFunction(param1, param2) {}
            "function_definition": {
                "query": """
                    (function_declaration name: (identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            # method under a class
            "method_definition": {
                "query": """
                    (method_definition name: [(property_identifier) (computed_property_name)] @method_name) @method_body
                """,
                "output_name": "method_name",
                "output_body": "method_body",
                "variant": TreeSitterNodeVariant.METHOD,
            },
            # example: class Animal {
            "class_definition": {
                "query": """
                    (class_declaration name: (_) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
            # example: class Zoo<T extends Animal>
            "class_definition_with_type_identifier": {
                "query": """
                    (class_declaration name: (type_identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
            # example: const arrowFunc = (x) => x * 2;
            "arrow_function_definition": {
                "query": """
                    (variable_declarator name: (identifier) @definition_name value: (arrow_function)) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
        },
        "reference": {
            "function_reference": {
                "query": """
                    (call_expression function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (call_expression function: (member_expression property: (property_identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (new_expression constructor: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            # covers <Test /> and <Test>...</Test>
            "jsx_component_reference": {
                "query": """
                    (jsx_self_closing_element name: (identifier) @reference_name)
                    (jsx_opening_element name: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
        },
    },
    # There are no functions in Ruby (only methods)
    "ruby": {
        "definition": {
            "method_definition": {
                "query": """
                    (method name: (identifier) @method_name) @method_body
                """,
                "output_name": "method_name",
                "output_body": "method_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "singleton_method_definition": {
                "query": """
                    (singleton_method name: (identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "class_definition": {
                "query": """
                    (class name: [(constant) (scope_resolution)] @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
            "module_definition": {
                "query": """
                    (module name: [(constant) (scope_resolution)] @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.MODULE,
            },
        },
        "reference": {
            "method_reference": {
                "query": """
                    (call method: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_call_reference": {
                "query": """
                    (call receiver: (_) operator: ["."] method: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (call
                      receiver: [(constant) (scope_resolution)] @reference_name
                      method: (identifier) @method
                      (#eq? @method "new"))
                """,
                "output_name": "reference_name",
            },
        },
    },
    "rust": {
        "definition": {
            "function_definition": {
                "query": """
                    (function_item name: (identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "method_definition": {
                "query": """
                    (impl_item 
                        body: (declaration_list 
                            (function_item name: (identifier) @method_name)) @method_body)
                """,
                "output_name": "method_name",
                "output_body": "method_body",
                "variant": TreeSitterNodeVariant.METHOD,
            },
            "associated_function_definition": {
                "query": """
                    (impl_item
                        body: (declaration_list
                            (function_item name: (identifier) @definition_name)) @definition_body)
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
        },
        "reference": {
            "function_reference": {
                "query": """
                    (call_expression function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (call_expression 
                        function: (field_expression field: (field_identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
            "associated_function_reference": {
                "query": """
                    (call_expression
                        function: (scoped_identifier name: (identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
        },
    },
    "go": {
        "definition": {
            "function_definition": {
                "query": """
                    (function_declaration name: (identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "method_definition": {
                "query": """
                    (method_declaration receiver: (parameter_list) name: (field_identifier) @method_name) @method_body
                """,
                "output_name": "method_name",
                "output_body": "method_body",
                "variant": TreeSitterNodeVariant.METHOD,
            },
        },
        "reference": {
            "any_reference": {
                "query": """
                    (call_expression (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
        },
    },
    "java": {  # Java does not have functions, only methods
        "definition": {
            "method_definition": {
                "query": """
                    (method_declaration name: (identifier) @method_name) @method_body
                """,
                "output_name": "method_name",
                "output_body": "method_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "constructor_definition": {
                "query": """
                    (constructor_declaration name: (identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "class_definition": {
                "query": """
                    (class_declaration name: (identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
            "record_definition": {
                "query": """
                    (record_declaration name: (identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
        },
        "reference": {
            "method_reference": {
                "query": """
                    (method_invocation name: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "constructor_reference": {
                "query": """
                    (object_creation_expression type: (type_identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (type_identifier) @reference_name
                """,
                "output_name": "reference_name",
            },
        },
    },
    "php": {
        "definition": {
            "function_definition": {
                "query": """
                    (function_definition name: (name) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "method_definition": {
                "query": """
                    (method_declaration name: (name) @method_name) @method_body
                """,
                "output_name": "method_name",
                "output_body": "method_body",
                "variant": TreeSitterNodeVariant.METHOD,
            },
            "class_definition": {
                "query": """
                    (class_declaration name: (name) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
            "trait_definition": {
                "query": """
                    (trait_declaration name: (name) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
        },
        "reference": {
            "function_reference": {
                "query": """
                    (function_call_expression function: (name) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (member_call_expression name: (name) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (object_creation_expression (name) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "static_method_reference": {
                "query": """
                    (scoped_call_expression scope: (name) name: (name) @reference_name)
                """,
                "output_name": "reference_name",
            },
        },
    },
    "cpp": {  # This covers both C and C++
        "definition": {
            "function_definition": {
                "query": """
                    (function_definition
                      declarator: (function_declarator
                        declarator: (identifier) @definition_name)) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.FUNCTION,
            },
            "method_definition": {
                "query": """
                    (function_definition
                      declarator: (function_declarator
                        declarator: (qualified_identifier
                          name: (identifier) @method_name))) @method_body
                """,
                "output_name": "method_name",
                "output_body": "method_body",
                "variant": TreeSitterNodeVariant.METHOD,
            },
            "class_definition": {
                "query": """
                    (class_specifier
                      name: (type_identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.CLASS,
            },
            "struct_definition": {
                "query": """
                    (struct_specifier
                      name: (type_identifier) @definition_name) @definition_body
                """,
                "output_name": "definition_name",
                "output_body": "definition_body",
                "variant": TreeSitterNodeVariant.STRUCT,
            },
        },
        "reference": {
            "function_reference": {
                "query": """
                    (call_expression
                      function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (call_expression
                      function: (field_expression
                        field: (field_identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (new_expression
                      type: (type_identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
        },
    },
    # "c#": {},
}
