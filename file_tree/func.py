# Author: weiwei

import os
from typing import List, Tuple

from file_tree.core import FileTree


def print_to_stream(lines: List[str], path: str = None):
    """
    Print strings to file if path is not None, else stdio.

    :param lines:
    :param path:
    :return:
    """
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            for one_line in lines:
                f.write(one_line + '\n')
    else:
        for one_line in lines:
            print(one_line)


def list_all_files(path: str, max_depth: int = -1):
    """
    List all files in the specified folder.

    :param path:
    :param max_depth:
    :return: [file path]
    """
    tree = FileTree.from_path(path)
    result = tree.list_all_files(max_depth)
    files = [os.path.join(x[0], x[1]) for x in result]

    return files


def list_all_folders(path: str, max_depth: int = -1):
    """
    List all folders in the specified folder.

    :param path:
    :param max_depth:
    :return: [folder path]
    """
    tree = FileTree.from_path(path)
    folders = tree.list_all_folders(max_depth)

    return folders


def count(path: str, max_depth: int = -1):
    """
    Count the number of folders and files for each sub folders in the specified folder.

    :param path:
    :param max_depth:
    :return: [(folder path, the number of folders, the number of files)]
    """
    tree = FileTree.from_path(path)
    count_list = tree.count(max_depth)

    return count_list


def tree(path: str, max_depth: int = -1):
    """
    List depth of every sub folder and file.
    :param path:
    :param max_depth:
    :return: [(depth, path)]
    """
    tree = FileTree.from_path(path)
    tree_list = tree.tree(max_depth)

    return tree_list


def tree_to_strs(tree_list: List[Tuple[int, str]]):
    """
    Tree to strings format.

    :param tree_list:
    :return: [str]
    """
    # node is last child or not
    last_child_list = [True]
    index_stack = [(0, 0)]
    for i in range(1, len(tree_list)):
        level = tree_list[i][0]

        while level <= index_stack[-1][1]:
            pre_index, pre_level = index_stack.pop()
            if level == pre_level:
                last_child_list[pre_index] = False

        last_child_list.append(True)
        index_stack.append((i, level))

    brother_str = '│   '
    last_brother_str = '    '
    child_str = '├── '
    last_child_str = '└── '
    lines = [tree_list[0][1]]
    prefix_stack = []
    for i in range(1, len(tree_list) - 1):
        level, path = tree_list[i]

        pre_level = tree_list[i - 1][0]

        if i != 1 and level > pre_level:  # ->
            prefix_stack.append(last_brother_str if last_child_list[i - 1] else brother_str)
        elif level == pre_level:  # --
            pass
        else:  # <-
            for _ in range(pre_level - level):
                prefix_stack.pop()

        cur_line = ''.join(prefix_stack) + (last_child_str if last_child_list[i] else child_str)
        lines.append(cur_line + path)
    level, path = tree_list[-1]
    cur_line = brother_str * (level - 1) + last_child_str
    lines.append(cur_line + path)

    return lines


def size(path: str, max_depth: int = -1):
    """
    Compute total size of every sub folder and file.

    :param path:
    :param max_depth:
    :param out_file:
    :return: [(path, size)]
    """
    tree = FileTree.from_path(path)
    size_list = tree.size(max_depth)

    return size_list


def change_paths(paths: List[str], old_root: str, new_root: str, mode: str = 'tree'):
    """
    Simulate move file paths to a new root, and return new path of files.

    :param paths:
    :param old_root:
    :param new_root:
    :param mode: choice in ['tree', 'flatten+simple', 'flatten+id']
    :return: [new path]
    """
    if mode == 'tree':
        new_paths = [x.replace(old_root, new_root) for x in paths]
    elif mode == 'flatten+simple':
        filenames = [os.path.split(x)[-1] for x in paths]
        new_paths = [os.path.join(new_root, x) for x in filenames]
    elif mode == 'flatten+id':
        filenames = [os.path.split(x)[-1] for x in paths]
        n = len(str(len(filenames)))
        template = '{:0' + str(n) + 'd}_{}'
        new_paths = [os.path.join(new_root, template.format(i, x)) for i, x in enumerate(filenames)]
    else:
        raise ValueError(f'mode is not support!')

    return new_paths
