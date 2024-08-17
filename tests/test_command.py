# Author: weiwei
import pytest
from tests import file_tree, file_tree2, path, line_targets, paths
from tests import read_file


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

    match_file = 'a/a/a.txt'
    os.system(f'python {file} match_files -p {path} -f {match_file} -o {out_file} -m filename')
    results.extend(read_file(out_file))

    os.system(f'python {file} group_by_ext -p {path} -o {out_file}')
    results.extend(read_file(out_file))

    assert len(results) == len(line_targets)
    for r, t in zip(results, line_targets):
        assert r.replace('\\', '/') == t.replace('\\', '/')


if __name__ == '__main__':
    pytest.main()
