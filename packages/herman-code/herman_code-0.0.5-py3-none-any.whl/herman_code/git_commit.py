"""
"""

import re
from pathlib import Path
from pprint import pformat, pprint
from typing import (Any,
                    Dict,
                    List,
                    Literal,
                    Tuple,
                    Union,
                    get_args)

from herman_code.code.bprint import bprint

# >>> Type definitions >>>
# NOTE Using the `type` statement doesn't work for TypeAlias objects which are later used with `typing.get_args`.
# NOTE The `type` statement is required for recursive TypeAlias object definitions.

# >>> Type definitions: Commit message list >>>
ListTreeNodeTypeBranch = Literal["b"]
ListTreeNodeTypeParent = Literal["p"]
ListTreeNodeTypeText = Literal["t"]
ListTreeNodeTypeFile = Literal["f"]

type ListTreeNodeType = Union[ListTreeNodeTypeBranch,
                              ListTreeNodeTypeParent,
                              ListTreeNodeTypeText,
                              ListTreeNodeTypeFile]

type NestedList = List[Union[Tuple[ListTreeNodeType,
                                   str],
                             NestedList]]

ParsedListKeyName = Literal["list_parsed"]
type ParsedListLeaf    = str
type ParsedListChild   = List[Union[ParsedListLeaf,
                                    Dict[str,
                                         Union[ParsedListChild,
                                               None]]]]
type ParsedList        = Dict[ParsedListKeyName, ParsedListChild]

# <<< Type definitions: Commit message list <<<

# ::: Type definitions: Staged file and tracked files lists :::
type ParsedTrackedFileChange  = Literal["deleted",
                                        "modified",
                                        "new file",
                                        "renamed"]
type ParsedTrackedFile        = Tuple[ParsedTrackedFileChange,
                                      str]
type ParsedStagedFileList     = List[ParsedTrackedFile]
type ParsedNotTrackedFileList = List[ParsedTrackedFile]

# :::  Type definitions: Parsed Git commit edit message :::
GitCommitEditMsgParts = Literal["1_title",
                                "2_text",
                                "3_list",
                                "4_boilerplate",
                                "5_branch",
                                "6_branch_status",
                                "7_remote_branch",
                                "8_num_commits",
                                "9_staged",
                                "10_not_staged",
                                "11_not_tracked"]
git_commit_editmsg_parts = get_args(GitCommitEditMsgParts)
KEY_TITLE_0         = "title"
KEY_TEXT_0          = "text"
KEY_LIST_0          = "list"
KEY_BOILERPLATE_0   = "boilerplate"
KEY_BRANCH_0        = "branch"
KEY_BRANCH_STATUS_0 = "branch_status"
KEY_REMOTE_BRANCH_0 = "remote_branch"
KEY_NUM_COMMITS_0   = "num_commits"
KEY_STAGED_0        = "staged"
KEY_NOT_STAGED_0    = "not_staged"
KEY_NOT_TRACKED_0   = "not_tracked"

KEY_TITLE_1         = git_commit_editmsg_parts[0]
KEY_TEXT_1          = git_commit_editmsg_parts[1]
KEY_LIST_1          = git_commit_editmsg_parts[2]
KEY_BOILERPLATE_1   = git_commit_editmsg_parts[3]
KEY_BRANCH_1        = git_commit_editmsg_parts[4]
KEY_BRANCH_STATUS_1 = git_commit_editmsg_parts[5]
KEY_REMOTE_BRANCH_1 = git_commit_editmsg_parts[6]
KEY_NUM_COMMITS_1   = git_commit_editmsg_parts[7]
KEY_STAGED_1        = git_commit_editmsg_parts[8]
KEY_NOT_STAGED_1    = git_commit_editmsg_parts[9]
KEY_NOT_TRACKED_1   = git_commit_editmsg_parts[10]

type ParsedGitCommitEditMsg = Dict[GitCommitEditMsgParts, Any]

# <<< Type definitions <<<

# ::: Regular expression patterns :::

PATTERN_COMMIT_EDITMSG = r"""(?msx:
                             \A
                             (?P<title>^.+?)\n
                             (?P<text>^.+?)\n
                             (?P<list>^- .+?)
                             # Capture all the whitespace between the last list element 
                             # and the boilerplate
                             (?:\W+)
                             (?P<boilerplate>
                             \#\ Please\ enter\ the\ commit\ message\ for\ your\ changes\.\ Lines\ starting\n
                             \#\ with\ '\#'\ will\ be\ ignored,\ and\ an\ empty\ message\ aborts\ the\ commit\.\n
                             \#\n)
                             \#\ On\ branch\ 
                             (?P<branch>.+)\n
                             \#\ Your\ branch\ is\ 
                             (?P<branch_status>.+)\ 
                             (?:with|of)\ '
                             (?P<remote_branch>.+)'
                             (\ by\ 
                             (?P<num_commits>\d+)
                             \ commit[s]?)?
                             \.\n
                             (\#\ \ \ \(use\ "git\ push"\ to\ publish\ your\ local\ commits\)\n)?
                             \#\n
                             \#\ Changes\ to\ be\ committed:\n
                             (?P<staged>.+?)
                             \#\n
                             (?:
                               \#\ Changes\ not\ staged\ for\ commit:\n
                               (?P<not_staged>.+?)
                               \#\n
                             )?
                             (?:
                               \#\ Untracked\ files:\n
                               (?P<not_tracked>.+)
                               \#\n
                             )?
                             \Z
                             )"""

PATTERN_EDITMSG_TRACKED = r"""(?x:
                              \#\t(?P<status>(?:deleted)|(?:modified)|(?:new\ file)|(?:renamed)):[ ]+
                              (?P<file>.+)\n
                              )"""

PATTERN_EDITMSG_UNTRACKED = r"""(?x:
                                \#\t(?P<file>.+)\n
                                )"""

# >>> Define constants from TypeAlias objects >>>
# NOTE We assume some of the TypeAlias objects to have only one argument, so we index accordingly the tuple result.

# ::: Define element types in the graph structure of a git commit message nested list :::
LIST_TREE_NODE_TYPE_BRANCH: ListTreeNodeTypeBranch = get_args(tp=ListTreeNodeTypeBranch)[0]
LIST_TREE_NODE_TYPE_PARENT: ListTreeNodeTypeParent = get_args(tp=ListTreeNodeTypeParent)[0]
LIST_TREE_NODE_TYPE_TEXT: ListTreeNodeTypeText     = get_args(tp=ListTreeNodeTypeText)[0]
LIST_TREE_NODE_TYPE_FILE: ListTreeNodeTypeFile     = get_args(tp=ListTreeNodeTypeFile)[0]

# ::: Define dictionary key name for parsed commit message nested list :::
KEY_PARSED_LIST: ParsedListKeyName = get_args(tp=ParsedListKeyName)[0]

# <<< Define constants from TypeAlias objects <<<


def recursive_split(string_: str,
                    lvl: int = 0,
                    parent: Union[str, None] = None,
                    it: int = 0,
                    verbose: int = 0) -> NestedList:
    """
    Splits text with a specific format into a nested list of strings.

    The format has the following criteria:

    1. It is a list with entries being lead by dashes (`-`) or plus signs 
       (`+`).
    2. Entries that begin with a dash are called "dashed" or "text" entries, 
       because they are assumed to contain text.
    3. Entries that begin with a plus sign are called "plussed" or "file 
       path" entries, because they are assumed to contain just one relative 
       or absolute file path, or one file path pointing to another, e.g. 
       `dir_1/fname.py -> dir_2/fname.py`.
    4. Dashed entries must be lead by 0 spaces or a number of spaces which is 
       a multiple of 2 and then followed by exactly one space. No other 
       whitespace characters are allowed
    5. Plussed entries must be lead by a number of spaces which is 
       a multiple of 2 and then followed by exactly one space. No other 
       whitespace characters are allowed
    6. Entries, either dashed or plussed, which are indented below another 
       entry, are called child entries. Therefore, it is implied there is a 
       graph relationship in the structure of this list. Graph terms are 
       used in the documentation of this module, e.g. parent, child, sister, 
       root, branch, leaf, node, etc.
    7. Plussed entries cannot be sisters to dashed entries.
    8. Entries can only be separated by one newline character, not counting 
       any leading spaces.
       - So, for example, the string `- Hello.\\n- World` represents two 
       sister entries.
       - The string `- Hello.\\n  - World` represents a parent and a child 
       entry, respectively. So does `- Hello.\\n  + world.txt`.

    The following are numbered examples of the format:

    (1)
    - Text
    - Text

    (2)
    - Text
      + File path
    - Text

    (3)
    - Text
      - Text
        + File path
    - Text

    The following are numbered examples of un-allowed formats:

    (1)
    - Text
    + File Path

    (2)
    - Text
      + File path
        - Text
    
    (3)
    - Text
      + File path
        + File path

    (4)
    - Text

    - Text

    (5)
    -  Text
    - Text

    (6)
    - Text
      - Text
      + File path
    """
    prefix_1 = lvl * 2 * " "

    if verbose > 0:
        print(f"{prefix_1}lvl {lvl}")

    li_1 = re.split(pattern=fr"\n{prefix_1}(?:-|\+) ",
                    string=string_)

    li_1_1 = re.split(pattern=fr"\n{prefix_1}- ",
                      string=string_)
    li_1_2 = re.split(pattern=fr"\n{prefix_1}\+ ",
                      string=string_)

    if verbose > 0:
        header = f"{prefix_1}{">" * 20}"
        footer = f"{prefix_1}{"<" * 20}"
        for li_1_ in [li_1, li_1_1, li_1_2]:
            print(header)
            bprint(obj=li_1_,
                   prefix=prefix_1)
            print(footer)

    len_li_1 = len(li_1)

    if len_li_1 == 1:
        # Not split implies a terminal node (leaf) has been reached.

        # Determine if terminal text, terminal file, or non-terminal text.
        if it == 1:
            if parent == "text":
                # Non-terminal text
                li_2 = (LIST_TREE_NODE_TYPE_BRANCH,
                        li_1[0])
            elif parent == "file":
                # Non-terminal text, parent of files
                li_2 = (LIST_TREE_NODE_TYPE_PARENT,
                        li_1[0])
        elif it > 1:
            li_2 = li_1_1[0]
            if parent == "text":
                # Terminal text
                li_2 = (LIST_TREE_NODE_TYPE_TEXT,
                        li_1[0])
            elif parent == "file":
                # Terminal file
                # li_1_new = re.sub(pattern=r"\n", repl="", string=li_1[0])  # NOTE If the last item in a list is a terminal file, it will have a trailing newline.
                li_2 = (LIST_TREE_NODE_TYPE_FILE,
                        li_1[0])
        else:
            raise Exception("This should not happen.")
    elif len_li_1 > 1:
        # A split implies we are still on a non-terminal node (branch).

        # Determine if terminal text or terminal file
        if len_li_1 == len(li_1_1):
            # Terminal text
            parent = "text"
        elif len_li_1 == len(li_1_2):
            # Terminal file
            parent = "file"
        else:
            raise Exception("This should not happen.")

        li_2 = []
        header = f"{"  " + prefix_1}{">" * 20}"
        footer = f"{"  " + prefix_1}{"<" * 20}"
        prefix_2 = prefix_1 + (2 * " ")
        for it, string_el in enumerate(li_1, start=1):
            if verbose > 0:
                print(header)
                bprint(obj=string_el,
                       prefix=prefix_2)
                print(footer)

            li = recursive_split(string_=string_el,
                                lvl=lvl+1,
                                parent=parent,
                                it=it,
                                verbose=verbose)
            li_2.append(li)
    else:
        raise Exception("An unexpected error occured.")

    return li_2


def li_to_di(nested_list: NestedList,
             parent_name: Any = None,
             lvl: int = 0) -> ParsedList:
    """
    Recurses through a nested list to convert it into a nested dictionary.

    We assume a particular structure of the nested list, namely that the nested list `nested_list` is created such that all child lists are of length of at least 2, with the first element being the parent, and the subsequent elements being the children.
    """

    if lvl == 0:
        key_name = KEY_PARSED_LIST
    elif lvl > 0:
        key_name = parent_name
    else:
        raise ValueError("Parameter `lvl` must be a non-negative integer.")
    di = {key_name: None}
    li_parsed = []
    for el in nested_list:
        if isinstance(el, list):
            di_child = li_to_di(nested_list=el[1:],
                                parent_name=el[0][1],
                                lvl=lvl+1)
        elif isinstance(el, tuple):
            type_ = el[0]
            content = el[1]
            if type_ in [LIST_TREE_NODE_TYPE_BRANCH,
                         LIST_TREE_NODE_TYPE_PARENT]:
                raise Exception("An unexpected error occured.")
            elif type_ == LIST_TREE_NODE_TYPE_TEXT:
                di_child = {content: None}
            elif type_ == LIST_TREE_NODE_TYPE_FILE:
                di_child = content
            else:
                message = f"Terminal node type values must be one of {LIST_TREE_NODE_TYPE_BRANCH,
                                                                      LIST_TREE_NODE_TYPE_PARENT,
                                                                      LIST_TREE_NODE_TYPE_TEXT,
                                                                      LIST_TREE_NODE_TYPE_FILE}."
                raise Exception(message)
        else:
            raise Exception("Nested list elements must be string or list.")
        li_parsed.append(di_child)
    di[key_name] = li_parsed

    return di


def parse_list(string_: str,
               verbose: int = 0) -> ParsedList:
    """
    """
    # We define list elements as starting with `\n`, some whitespace, either a `-` or `.`, and then a single space. Therefore we add a single newline to the list string which was removed from dividing the commit message into parts.
    string_ = "\n" + string_

    li = recursive_split(string_=string_,
                         verbose=verbose)

    # Remove empty string from leading `\n`
    li = li[1:]

    # Turn nested list into nested dictionary
    di = li_to_di(nested_list=li)

    return di


def check_is_renamed(string_: str) -> Tuple[bool,
                                            Union[Tuple[str,
                                                        str],
                                                  Tuple[()]]]:
    """
    Determines if a string from a parsed commit message list indicates a 
    renamed file, e.g., `dir_1/fname.text -> dir_2/fname.text`
    """
    pattern = r"^(.+) -> (.+$)"
    match_obj = re.match(pattern=pattern,
                         string=string_)
    if match_obj:
        result = True, match_obj.groups()
    else:
        result = False, ()
    return result


def get_files_from_parsed_list(list_parsed_x: Union[ParsedList, ParsedListChild],
                               lvl: int = 0) -> List[str]:
    """
    """
    # NOTE we use `list_parsed_x` to differentiate from `list_parsed`, because the latter is strictly of type `ParsedList` while the former can be either of type `ParsedList` or `ParsedListChild`.

    if lvl == 0:
        li_0: ParsedListChild = list_parsed_x[KEY_PARSED_LIST]
    elif lvl > 0:
        li_0: ParsedListChild = list_parsed_x
    else:
        raise Exception("Parameter `lvl` must be a non-negative integer.")
    
    li_1 = []
    for el in li_0:
        if isinstance(el, dict):
            el : ParsedListChild = el
            key: str             = list(el.keys())[0]
            val: ParsedListChild = el[key]
            if isinstance(val, type(None)):
                pass
            elif isinstance(val, list):
                child_li = get_files_from_parsed_list(list_parsed_x=val,
                                                      lvl=lvl+1)
                li_1.extend(child_li)
            else:
                raise Exception("The parsed list dictionary values must be one of {list, None}.")
        elif isinstance(el, str):
            el: ParsedListLeaf = el
            is_renamed, tu = check_is_renamed(el)  # NOTE Hopefuly we have no file paths that contain `->`
            if is_renamed:
                li_1.extend(list(tu))
            else:
                li_1.append(el)
        else:
            raise Exception("The parsed list object children must be one of {dict, str}.")
    
    return li_1


def get_files_from_parsed_staged(staged_parsed: ParsedStagedFileList) -> List[str]:
    """
    """
    sorted([tu[1] for tu in staged_parsed])
    li = []
    for tu in staged_parsed:
        if tu[0] == "renamed":
            _, (fp1, fp2) = check_is_renamed(tu[1])
            li.extend([fp1, fp2])
        else:
            li.append(tu[1])
    return li


def split_git_commit_editmsg(filepath: Path) -> Union[Dict[str, str | Any], None]:
    """
    Parse a commit message that was written in the Herman's Code format into its main parts.
    """

    with open(file=filepath, mode="r") as file_obj:
        text = file_obj.read()
    
    pattern = re.compile(pattern=PATTERN_COMMIT_EDITMSG)

    match_obj = pattern.search(string=text)

    if match_obj:
        result = match_obj.groupdict()
    else:
        result = None

    return result


def parse_git_commit_editmsg(filepath: Path,
                             verbose: int = 0) -> ParsedGitCommitEditMsg:
    """
    Parse a commit message that was written in the Herman's Code format.
    """

    parts = split_git_commit_editmsg(filepath=filepath)

    # ::: 1 ::: Unpack results
    if parts:
        title         = parts[KEY_TITLE_0]
        text          = parts[KEY_TEXT_0]
        list_         = parts[KEY_LIST_0]
        boilerplate   = parts[KEY_BOILERPLATE_0]
        branch        = parts[KEY_BRANCH_0]
        remote_branch = parts[KEY_REMOTE_BRANCH_0]
        staged        = parts[KEY_STAGED_0]
        not_staged    = parts[KEY_NOT_STAGED_0]
        not_tracked   = parts[KEY_NOT_TRACKED_0]

        results = {KEY_TITLE_1: title,
                   KEY_TEXT_1: text,
                   KEY_LIST_1: list_,
                   KEY_BOILERPLATE_1: boilerplate,
                   KEY_BRANCH_1: branch,
                   KEY_REMOTE_BRANCH_1: remote_branch,
                   KEY_STAGED_1: staged,
                   KEY_NOT_STAGED_1: not_staged,
                   KEY_NOT_TRACKED_1: not_tracked}

        is_commit_format_2 = KEY_BRANCH_STATUS_0 in parts.keys() and KEY_NUM_COMMITS_0 in parts.keys()
        if is_commit_format_2:
            branch_status = parts["branch_status"]
            num_commits   = parts["num_commits"]

            results[KEY_BRANCH_STATUS_1] = branch_status
            results[KEY_NUM_COMMITS_1]   = num_commits

    else:
        fp = Path(filepath).absolute()
        raise Exception(f"Could not parse the selected file: {fp}")
    
    if verbose > 0:
        pprint(results)

    # ::: 2 ::: Parse list
    list_parsed = parse_list(string_=list_,
                             verbose=verbose-1)
    results[KEY_LIST_1] = list_parsed

    # ::: 3 ::: Parse staged files
    pattern_2 = re.compile(pattern=PATTERN_EDITMSG_TRACKED)
    staged_parsed = pattern_2.findall(string=staged)
    results[KEY_STAGED_1] = staged_parsed

    # ::: 4 ::: Parsed files not staged
    if not_staged:
        pattern_3 = re.compile(pattern=PATTERN_EDITMSG_TRACKED)
        not_staged_parsed = pattern_3.findall(string=not_staged)
    else:
        not_staged_parsed = None
    results[KEY_NOT_STAGED_1] = not_staged_parsed

    # ::: 5 ::: Parse untracked files
    if not_tracked:
        pattern_3 = re.compile(pattern=PATTERN_EDITMSG_UNTRACKED)
        not_tracked_parsed = pattern_3.findall(string=not_tracked)
    else:
        not_tracked_parsed = None
    results[KEY_NOT_TRACKED_1] = not_tracked_parsed

    return results

def check_git_commit_editmsg(filepath: Path,
                             verbose: int = 0) -> Tuple[Dict, Dict, Dict]:
    """
    Checks if a Git commit message addressed changes in all files
    """
    parsed_message = parse_git_commit_editmsg(filepath=filepath,
                                              verbose=verbose-1)

    staged_parsed = parsed_message[KEY_STAGED_1]
    list_parsed   = parsed_message[KEY_LIST_1]

    # Get list of files from parsed commit message list
    files_from_list = get_files_from_parsed_list(list_parsed_x=list_parsed)

    # Get list of files from parsed list of staged files
    files_from_staged = get_files_from_parsed_staged(staged_parsed=staged_parsed)

    # Make sure each staged file was mentioned in the list and vice versa
    check_staged_in_list = {}
    check_staged_ni_list = []  # Not-in
    for fpath in files_from_staged:
        result = fpath in files_from_list
        check_staged_in_list[fpath] = result
        if not result:
            check_staged_ni_list.append(fpath)

    check_list_in_staged = {}
    check_list_ni_staged = []  # Not-in
    for fpath in files_from_list:
        result = fpath in files_from_staged
        check_list_in_staged[fpath] = result
        if not result:
            check_list_ni_staged.append(fpath)

    # Package results
    result_medium = {"num_staged_in_list": sum(check_staged_in_list.values()),
                     "num_list_in_staged": sum(check_list_in_staged.values()),
                     "num_staged": len(files_from_staged)}

    result_short = result_medium["num_list_in_staged"] == result_medium["num_staged_in_list"] == result_medium["num_staged"]

    result_long  = {"staged_in_list": check_staged_in_list,
                    "staged_ni_list": check_staged_ni_list,
                    "list_in_staged": check_list_in_staged,
                    "list_ni_staged": check_list_ni_staged}
    
    # Print results
    if verbose > 0:
        results = f"""\

{result_short}

{pformat(result_medium)}

{pformat(result_long)}"""

        print(results)

    # Return results
    return result_short, result_medium, result_long


def mf_1(args):
    """
    """
    return parse_git_commit_editmsg(filepath=args.file_path,
                                    verbose=args.v)


def mf_2(args):
    """
    """
    return check_git_commit_editmsg(filepath=args.file_path,
                                    verbose=args.v)
