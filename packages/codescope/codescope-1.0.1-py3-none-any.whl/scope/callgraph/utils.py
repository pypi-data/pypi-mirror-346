# Standard library
import os
import shutil
from typing import List
import hashlib
import tempfile
import json

# Third party
from multilspy import SyncLanguageServer
from multilspy.multilspy_config import MultilspyConfig
from multilspy.multilspy_logger import MultilspyLogger

# Local
from scope.callgraph.resources import EXT_TO_LANGUAGE_DATA
from scope.callgraph.constants import (
    LANGUAGE_TO_LSP_LANGUAGE_MAP,
)
from scope.callgraph.dtos import Definition, Range
# from scope.dtos import Reference


def is_file_empty(path):
    """
    Check if a file is empty by examining its size.

    Args:
        path (str): Path to the file to check.

    Returns:
        bool: True if the file is empty (size is 0), False otherwise.
    """
    return os.stat(path).st_size == 0


def root_contains_path(root_path, path):
    """
    Check if a path is contained within a root directory's scope.

    This function prevents quirky behavior where the LSP returns definitions from
    things like .venv by ensuring the path is within the root directory's scope.

    Args:
        root_path (str): The root directory path.
        path (str): The path to check if it's contained within root_path.

    Returns:
        bool: True if the path is contained within root_path, False otherwise.
    """
    return os.path.commonpath([path, root_path]) == root_path


def get_all_paths_from_root_relative(root_path):
    """
    Get all file paths within a root directory, both absolute and relative.

    Args:
        root_path (str): The root directory to search in.

    Returns:
        tuple: A tuple containing two lists:
            - List of absolute paths
            - List of relative paths
    """
    abs_paths, rel_paths = [], []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            abs_path = os.path.join(root, file)
            relpath = os.path.relpath(abs_path, root_path)
            abs_paths.append(abs_path)
            rel_paths.append(relpath)
    return abs_paths, rel_paths


def create_lsp_client_instance(root_path, language) -> SyncLanguageServer:
    """
    Create a new instance of the Language Server Protocol client.

    Args:
        root_path (str): The root directory path for the LSP client.
        language (str): The programming language to use.

    Returns:
        SyncLanguageServer: An initialized LSP client instance.
    """
    abs_root_path = os.path.abspath(root_path)
    config = MultilspyConfig.from_dict({"code_language": language})
    logger = MultilspyLogger()
    return SyncLanguageServer.create(config, logger, abs_root_path)


def get_language_from_ext(path):
    """
    Determine the programming language and related information from a file extension.

    Args:
        path (str): The file path to analyze.

    Returns:
        tuple: A tuple containing:
            - LSP language identifier
            - Language mode
            - Boolean indicating if the file is code
    """
    root, ext = os.path.splitext(path)
    language_info = EXT_TO_LANGUAGE_DATA.get(ext, {})
    is_code = language_info.get("is_code", False)
    language = language_info.get("language_mode", None)
    lsp_language = LANGUAGE_TO_LSP_LANGUAGE_MAP.get(language, None)
    return lsp_language, language, is_code


def keep_file_for_language(root, file, language):
    """
    Determine if a file should be kept based on its language and type.

    Args:
        root (str): The root directory path.
        file (str): The file name to check.
        language (str): The target language to filter by.

    Returns:
        bool: True if the file should be kept, False otherwise.
    """
    file_language, _, is_code = get_language_from_ext(file)
    if file_language == language and is_code:
        return True
    match language:
        case "javascript" | "typescript":
            if file.endswith("config.json") or file.endswith("package.json"):
                print("CallGraphBuilder :: keeping file: ", os.path.join(root, file))
                return True
        case _:
            return False


def copy_and_split_root_by_language_group(abs_root_path):
    """
    Copy and split a root directory into separate directories based on programming languages.

    This function creates separate copies of the root directory for each detected
    programming language, keeping only relevant files for each language.

    Args:
        abs_root_path (str): The absolute path to the root directory.

    Returns:
        list: List of tuples containing (copy_path, language) for non-empty directories.
    """
    abs_paths, _ = get_all_paths_from_root_relative(abs_root_path)
    languages = set()

    for p in abs_paths:
        lsp_language, language, is_code = get_language_from_ext(p)
        if is_code:
            languages.add(lsp_language)
    languages = [lang for lang in languages if lang]

    copy_paths = []
    # copy the root directory into a temporary directory per language
    for _ in range(len(languages)):
        tmp_parent_dir = tempfile.mkdtemp(prefix="scope_")
        shutil.copytree(abs_root_path, tmp_parent_dir, dirs_exist_ok=True)
        copy_paths.append(tmp_parent_dir)

    for copy_path, language in zip(copy_paths, languages):
        for root, dirs, files in os.walk(copy_path):
            for file in files:
                if keep_file_for_language(root, file, language):
                    continue
                else:
                    # print(f"removing file: {os.path.join(root, file)}")
                    os.remove(os.path.join(root, file))

    # remove copy_paths that only have directories and no files
    nonempty_copy_paths = []
    for copy_path, language in zip(copy_paths, languages):
        files_set = set()
        for root, dirs, files in os.walk(copy_path):
            for file in files:
                files_set.add(file)
        if not files_set:
            print(f"copy_path: {copy_path} is empty")
            shutil.rmtree(copy_path)
            continue
        nonempty_copy_paths.append((copy_path, language))

    return nonempty_copy_paths


def convert_to_relative_path(abs_path, root_path):
    """
    Convert an absolute path to a relative path based on a root path.

    Args:
        abs_path (str): The absolute path to convert.
        root_path (str): The root path to use as reference.

    Returns:
        str: The relative path, or the original absolute path if conversion fails.
    """
    # Ensure both paths are absolute
    abs_path = os.path.abspath(abs_path)
    root_path = os.path.abspath(root_path)
    try:
        rel_path = os.path.relpath(root_path, start=abs_path)
        return rel_path
    except ValueError as e:
        print(f"Error converting absolute path to relative path: {e}")
        return abs_path


def flatten(xss):
    """
    Flatten a list of lists into a single list.

    Args:
        xss (list): A list of lists to flatten.

    Returns:
        list: A flattened list containing all elements from the input lists.
    """
    return [x for xs in xss for x in xs]


## CALLGRAPH SPECIFIC UTILS


def get_containing_def_for_ref(defs: List[Definition], ref_range: Range):
    """
    Find the smallest definition that contains a given reference range.

    Args:
        defs (List[Definition]): List of definitions to search through.
        ref_range (Range): The reference range to find a containing definition for.

    Returns:
        Definition | None: The smallest definition containing the reference range,
                          or None if no containing definition is found.
    """
    # find smallest range that contains ref
    containing_defs: List[Definition] = []
    for defn in defs:
        if defn.snippet_range.contains(ref_range):
            containing_defs.append(defn)
    if not containing_defs:
        return None
    return min(containing_defs, key=lambda x: x.snippet_range.height())


def get_containing_ref_for_ref(refs: list, ref_range: Range):
    """
    Find the reference that contains another reference range.
    
    Note: This function is not yet implemented. It will be useful for jsx/tsx
    or when passing functions as arguments.

    Args:
        refs (list): List of references to search through.
        ref_range (Range): The reference range to find a containing reference for.

    Returns:
        None: Currently not implemented.
    """
    # TODO: Implement this. Useful in jsx/tsx or passing functions as arguments.
    # TODO: also figure out circular import issue w/ refs: List[Reference]
    pass


def get_node_id_for_viz(defn: Definition):
    """
    Generate a unique node ID for visualization from a definition.

    Args:
        defn (Definition): The definition to generate a node ID for.

    Returns:
        str: A unique node ID string containing path and range information.
    """
    node_id = f"{defn.path}::"
    node_id += f"{defn.range.start_line}-{defn.range.end_line}::"
    node_id += f"{defn.range.start_column}-{defn.range.end_column}"
    return node_id


def stable_hash(obj: dict, as_int=False, slice_size=16) -> str | int:
    """
    Create a stable hash from a dictionary.

    The hash is created by:
    1. Converting the dictionary to a JSON string with sorted keys
    2. Encoding to bytes
    3. Generating a SHA-256 hash

    Args:
        obj (dict): The dictionary to hash.
        as_int (bool, optional): Whether to return the hash as an integer. Defaults to False.
        slice_size (int, optional): Size of the hash slice when returning as integer. Defaults to 16.

    Returns:
        str | int: The hash as a hexadecimal string or integer.

    Raises:
        ValueError: If slice_size is negative when as_int is True.
    """
    # Convert dict to JSON string with sorted keys for consistency
    json_str = json.dumps(obj, sort_keys=True)
    # Create SHA-256 hash
    bytestr = hashlib.sha256(json_str.encode("utf-8")).hexdigest()
    if as_int:
        if slice_size is None:
            return int(bytestr, 16)
        if slice_size > 0:
            return int(bytestr[:slice_size], 16)
        raise ValueError(f"Invalid slice_size: {slice_size}")
    return bytestr
