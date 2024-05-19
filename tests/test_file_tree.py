# Author: weiwei
import collections

import pytest

from file_tree import func
from tests import file_tree, file_tree2, path, read_file, line_targets, paths


def test_from_strings(file_tree, file_tree2):
    def compare_tree(result_root, target_root):
        assert result_root.path.replace('\\', '/') == target_root.path.replace('\\', '/')
        assert result_root.depth == target_root.depth
        nodes1 = result_root.nodes
        nodes2 = target_root.nodes
        assert nodes1 == nodes2 or len(nodes1) == len(nodes2)
        nodes1 = nodes1 if nodes1 is not None else []
        nodes2 = nodes2 if nodes2 is not None else []
        nodes1 = sorted(nodes1, key=lambda x: x.path.replace('\\', '/'))
        nodes2 = sorted(nodes2, key=lambda x: x.path.replace('\\', '/'))
        for x1, x2 in zip(nodes1, nodes2):
            compare_tree(x1, x2)

    src_root, dst_root = file_tree2, file_tree
    compare_tree(src_root, dst_root)


def test_list_all_files(file_tree):
    def compare(result, target):
        assert len(result) == len(target)
        for r, t in zip(result, target):
            assert r[0].replace('\\', '/') == t[0]
            assert r[1] == t[1]

    # test depth -1
    target = [('../resources', 'a.txt'), ('../resources/a', 'a.txt'),
              ('../resources/a/a', 'a.txt'), ('../resources/a/a', 'b.txt')]
    result = file_tree.list_all_files()
    # print(result)
    compare(result, target)

    # test depth 0
    target = []
    result = file_tree.list_all_files(max_depth=0)
    # print(result)
    compare(result, target)

    # test depth 1
    target = [('../resources', 'a.txt')]
    result = file_tree.list_all_files(max_depth=1)
    # print(result)
    compare(result, target)

    # test depth 2
    target = [('../resources', 'a.txt'), ('../resources/a', 'a.txt')]
    result = file_tree.list_all_files(max_depth=2)
    # print(result)
    compare(result, target)

    # test depth 3
    target = [('../resources', 'a.txt'), ('../resources/a', 'a.txt'),
              ('../resources/a/a', 'a.txt'), ('../resources/a/a', 'b.txt')]
    result = file_tree.list_all_files(max_depth=3)
    # print(result)
    compare(result, target)


def test_list_all_folders(file_tree):
    def compare(result, target):
        assert len(result) == len(target)
        for r, t in zip(result, target):
            assert r.replace('\\', '/') == t

    # test depth -1
    target = ['../resources', '../resources/a', '../resources/a/a', '../resources/a/b', '../resources/b',
              '../resources/b/a', '../resources/c']
    result = file_tree.list_all_folders()
    # print(result)
    compare(result, target)


def test_count(file_tree):
    def compare(result, target):
        assert len(result) == len(target)
        for r, t in zip(result, target):
            assert r[0].replace('\\', '/') == t[0]
            assert r[1] == t[1]
            assert r[2] == t[2]

    # test depth -1
    target = [('../resources', 6, 4),
              ('../resources/a', 2, 3),
              ('../resources/a/a', 0, 2),
              ('../resources/a/b', 0, 0),
              ('../resources/b', 1, 0),
              ('../resources/b/a', 0, 0),
              ('../resources/c', 0, 0)]
    result = file_tree.count()
    compare(result, target)

    # test depth 1
    target = [('../resources', 6, 4),
              ('../resources/a', 2, 3),
              ('../resources/b', 1, 0),
              ('../resources/c', 0, 0)]
    result = file_tree.count(max_depth=1)
    compare(result, target)


def test_tree(file_tree):
    def compare(result, target):
        assert len(result) == len(target)
        for r, t in zip(result, target):
            assert r[0] == t[0]
            assert r[1].replace('\\', '/') == t[1]

    # test depth -1
    target = [(0, 'resources'), (1, 'a.txt'), (1, 'a'), (2, 'a.txt'), (2, 'a'),
              (3, 'a.txt'), (3, 'b.txt'), (2, 'b'), (1, 'b'), (2, 'a'), (1, 'c')]
    result = file_tree.tree()
    compare(result, target)

    # test depth 1
    target = [(0, 'resources'), (1, 'a.txt'), (1, 'a'), (1, 'b'), (1, 'c')]
    result = file_tree.tree(max_depth=1)
    compare(result, target)


def test_size(file_tree):
    def compare(result, target):
        assert len(result) == len(target)
        for r, t in zip(result, target):
            assert r[0].replace('\\', '/') == t[0]
            assert r[1] == t[1]

    # test depth -1
    target = [('../resources', 12), ('../resources/a.txt', 3), ('../resources/a', 9), ('../resources/a/a.txt', 3),
              ('../resources/a/a', 6), ('../resources/a/a/a.txt', 3), ('../resources/a/a/b.txt', 3),
              ('../resources/a/b', 0), ('../resources/b', 0), ('../resources/b/a', 0), ('../resources/c', 0)]
    result = file_tree.size()
    compare(result, target)

    # test depth 1
    target = [('../resources', 12), ('../resources/a.txt', 3), ('../resources/a', 9),
              ('../resources/b', 0), ('../resources/c', 0)]
    result = file_tree.size(max_depth=1)
    compare(result, target)


def test_func(path, line_targets):
    func.list_all_files(path)
    func.list_all_folders(path)
    func.count(path)
    func.tree(path)
    func.size(path)

    # results = []
    # out_file = 'out.txt'
    # func.list_all_files(path)
    # results.extend(read_file(out_file))
    # func.list_all_folders(path)
    # results.extend(read_file(out_file))
    # func.count(path)
    # results.extend(read_file(out_file))
    # func.tree(path)
    # results.extend(read_file(out_file))
    # func.size(path)
    # results.extend(read_file(out_file))
    #
    # assert len(results) == len(line_targets)
    # for r, t in zip(results, line_targets):
    #     assert r == t


def test_command(path, line_targets):
    import os

    file = '../file_tree/main.py'
    path = '../resources'
    out_file = 'out.txt'

    results = []
    os.system(f'python {file} list_all_files -p {path} -o {out_file}')
    results.extend(read_file(out_file))
    os.system(f'python {file} list_all_folders -p {path} -o {out_file}')
    results.extend(read_file(out_file))
    os.system(f'python {file} count -p {path} -o {out_file}')
    results.extend(read_file(out_file))
    os.system(f'python {file} tree -p {path} -o {out_file}')
    results.extend(read_file(out_file))
    os.system(f'python {file} size -p {path} -o {out_file}')
    results.extend(read_file(out_file))
    new_path = 'tests'
    os.system(f'python {file} change_paths -p {path} -n {new_path} -o {out_file} -m flatten+id')
    results.extend(read_file(out_file))

    assert len(results) == len(line_targets)
    for r, t in zip(results, line_targets):
        assert r.replace('\\', '/') == t.replace('\\', '/')


def test_change_paths(paths):
    def compare(result, target):
        assert len(result) == len(target)
        for r, t in zip(result, target):
            assert r.replace('\\', '/') == t.replace('\\', '/')

    old_root = '../resources'
    new_root = 'tests'

    # test tree
    target = ['tests/a.txt', 'tests/a/a.txt', 'tests/a/a/a.txt', 'tests/a/a/b.txt']
    result = func.change_paths(paths, old_root, new_root, mode='tree')
    compare(result, target)

    target = ['tests/a.txt', 'tests/a.txt', 'tests/a.txt', 'tests/b.txt']
    result = func.change_paths(paths, old_root, new_root, mode='flatten+simple')
    compare(result, target)

    target = ['tests/0_a.txt', 'tests/1_a.txt', 'tests/2_a.txt', 'tests/3_b.txt']
    result = func.change_paths(paths, old_root, new_root, mode='flatten+id')
    compare(result, target)


if __name__ == '__main__':
    pytest.main()
