# Author: weiwei
import collections
import itertools
import os
from itertools import chain
from typing import List, Tuple


def get_file_size(file_path: str) -> int:
    """
    Get size of file.

    :param file_path:
    :return:
    """
    file_info = os.stat(file_path)
    file_size = file_info.st_size
    return file_size


class FileTree(object):
    def __init__(self, path: str, name: str = '', depth: int = 0):
        self.path = path
        self.depth = depth
        self.name = name
        self.exist = os.path.exists(path) or os.path.isdir(path)

        self.nodes = None

    @property
    def isdir(self):
        return self.nodes is not None

    @property
    def folders(self):
        return [x for x in self.nodes if x.isdir] if self.nodes else []

    @property
    def files(self):
        return [x for x in self.nodes if not x.isdir] if self.nodes else []

    @classmethod
    def from_path(cls, path: str, depth: int = 0):
        """
        Construct a file tree from specified root path

        :param path:
        :param depth:
        :return:
        """
        _, name = os.path.split(path)
        root = FileTree(path, name, depth)

        if os.path.exists(path) and os.path.isdir(path):
            filenames = sorted(os.listdir(path))
            nodes = [FileTree.from_path(os.path.join(path, p), root.depth + 1) for p in filenames]
            root.nodes = nodes
            root.nodes = root.files + root.folders
        # else:
        #     root.name = ''
        #     root.files = []
        #     root.folders = []

        return root

    @classmethod
    def from_strings(cls, strings: List[str], depth: int = 0):
        """
        Construct a file tree from list of path string
        :param strings:
        :param depth:
        :return:
        """
        strings = [x.replace('\\', '/') for x in strings]
        strings = [x.split('/') for x in strings]
        strings = sorted(strings, key=lambda x: (len(x), x))

        # find prefix
        i = 0
        while i < len(strings[0]):
            n = len(set(x[i] for x in strings))
            if n > 1:
                break
            i += 1
        prefix_idx = i

        # build a tree
        # create a root
        prefix = strings[0][:prefix_idx]
        root_path = '/'.join(prefix)
        root_name = prefix[-1] if prefix else ''
        root = FileTree(root_path, root_name, depth)
        # build children
        node_dict = {root_path: root}
        for x in strings:
            path = '/'.join(x)

            # create node
            if path in node_dict:
                continue
            parent, name = os.path.split(path)
            cur_depth = depth + len(x) - prefix_idx
            cur_node = FileTree(path, name, cur_depth)
            if os.path.exists(path) and os.path.isdir(path):
                cur_node.nodes = []
            node_dict[path] = cur_node

            # insert to parent node
            while parent not in node_dict:
                cur_path = parent
                childs = [cur_node]
                parent, name = os.path.split(cur_path)
                cur_depth -= 1
                cur_node = FileTree(parent, name, cur_depth)
                cur_node.nodes = childs
                node_dict[cur_path] = cur_node

            brother_node = node_dict[parent].nodes
            if brother_node is None:
                node_dict[parent].nodes = [cur_node]
            else:
                node_dict[parent].nodes.append(cur_node)

        return root

    def _stop(self, cur_depth, max_depth):
        if 0 <= max_depth < cur_depth:
            return True
        else:
            return False

    def list_all_files(self, max_depth: int = -1) -> List[Tuple[str, str]]:
        """
        List all files in the folder.

        :param max_depth:
        :return: [(file path, file name)]
        """
        # if 0 <= max_depth < self.depth:
        if self._stop(self.depth, max_depth):
            return []

        if self.isdir:
            files = []
            sub_files = [x.list_all_files(max_depth) for x in self.nodes]
        else:
            files = [os.path.split(self.path)]
            sub_files = []

        return list(chain(*[files, *sub_files]))

    def list_all_folders(self, max_depth: int = -1) -> List[str]:
        """
        List all folders in the folder.

        :param max_depth:
        :return: [folder path]
        """
        # if 0 <= max_depth < self.depth:
        if self._stop(self.depth, max_depth):
            return []

        if not self.isdir:
            return []

        path = self.path
        sub_dirs = [x.list_all_folders(max_depth) for x in self.nodes]

        return list(chain(*[[path], *sub_dirs]))

    def count(self, max_depth: int = -1) -> List[Tuple[str, int, int]]:
        """
        Count the number of folders and files in the folder and every sub folder.

        :param max_depth:
        :return: [(folder path, the number of folders, the number of files)]
        """
        folders, files = self.folders, self.files
        n_folders = len(folders)
        n_files = len(files)
        if len(folders) > 0:
            sub_items = [x.count(max_depth) for x in folders]
            n_folders += sum(x[0][1] for x in sub_items)
            n_files += sum(x[0][2] for x in sub_items)
        else:
            sub_items = []

        item = (self.path, n_folders, n_files)

        # if 0 <= max_depth < self.depth + 1:
        if self._stop(self.depth + 1, max_depth):
            sub_items = []

        return list(chain(*[[item], *sub_items]))

    def tree(self, max_depth: int = -1) -> List[Tuple[int, str]]:
        """
        List depth of every sub folder and file.

        :param max_depth:
        :return: [(depth, path)]
        """
        if self._stop(self.depth, max_depth):
            return []

        item = (self.depth, self.name)
        if self._stop(self.depth + 1, max_depth):
            return [item]

        if self.isdir:
            sub_items = [x.tree(max_depth) for x in self.nodes]
        else:
            sub_items = []

        return list(chain(*[[item], *sub_items]))

    def size(self, max_depth: int = -1) -> List[Tuple[str, int]]:
        """
        Compute total size of every sub folder and file.

        :param max_depth:
        :return: [(path, size)]
        """
        if self.isdir:
            sub_items = [x.size(max_depth) for x in self.nodes]
            total_size = sum(x[0][1] for x in sub_items)
            item = (self.path, total_size)
        else:
            sub_items = []
            item = (self.path, get_file_size(self.path))

        # if 0 <= max_depth < self.depth + 1:
        if self._stop(self.depth + 1, max_depth):
            sub_items = []

        return list(chain(*[[item], *sub_items]))
