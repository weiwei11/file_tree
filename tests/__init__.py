
import pytest
from file_tree import FileTree


@pytest.fixture
def path():
    return '../resources'


@pytest.fixture
def file_tree():
    return FileTree.from_path('../resources')


@pytest.fixture
def file_tree2():
    strings = [
        '../resources/a.txt',
        '../resources/a/a.txt',
        '../resources/a/a/a.txt',
        '../resources/a/a/b.txt',
        '../resources',
        '../resources/a',
        '../resources/a/a',
        '../resources/a/b',
        '../resources/b',
        '../resources/b/a',
        '../resources/c',
    ]
    return FileTree.from_strings(strings)


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines


@pytest.fixture
def line_targets():
    return read_file('./results.txt')


@pytest.fixture
def paths():
    return [
        '../resources/a.txt',
        '../resources/a/a.txt',
        '../resources/a/a/a.txt',
        '../resources/a/a/b.txt',
    ]
