# Author: weiwei
import argparse

from file_tree.func import *
from file_tree.func import print_to_stream


def change_paths_wrapper(path: str, new_path: str, mode: str = 'tree'):
    paths = list_all_files(path)
    return change_paths(paths, path, new_path, mode)


def match_files_wrapper(path: str, file: str, mode: str = 'filename'):
    paths = list_all_files(path)
    return match_files([file], paths, mode)[0][1]


def group_by_ext_wrapper(path: str):
    paths = list_all_files(path)
    return group_by_ext(paths)


cmd_dict = {
    'list_all_files': list_all_files,
    'list_all_folders': list_all_folders,
    'count': count,
    'tree': tree,
    'size': size,
    'change_paths': change_paths_wrapper,
    'match_files': match_files_wrapper,
    'group_by_ext': group_by_ext_wrapper,
}


def main():
    parser = argparse.ArgumentParser(description='A file tree tool.')
    sub_parser = parser.add_subparsers(dest='command')

    def add_args(cmd):
        cmd.add_argument('-p', '--path', type=str, required=True)
        cmd.add_argument('-d', '--max_depth', type=int, required=False, default=-1)
        cmd.add_argument('-o', '--out_file', type=str, required=False)

    # list_all_files
    sub_cmd = sub_parser.add_parser('list_all_files')
    add_args(sub_cmd)
    # list_all_folders
    sub_cmd = sub_parser.add_parser('list_all_folders')
    add_args(sub_cmd)
    # count
    sub_cmd = sub_parser.add_parser('count')
    add_args(sub_cmd)
    # tree
    sub_cmd = sub_parser.add_parser('tree')
    add_args(sub_cmd)
    # size
    sub_cmd = sub_parser.add_parser('size')
    add_args(sub_cmd)
    # change paths
    sub_cmd = sub_parser.add_parser('change_paths')
    sub_cmd.add_argument('-p', '--path', type=str, required=True)
    sub_cmd.add_argument('-n', '--new_path', type=str, required=True)
    sub_cmd.add_argument('-o', '--out_file', type=str, required=False)
    sub_cmd.add_argument('-m', '--mode', type=str, required=False)
    # match files
    sub_cmd = sub_parser.add_parser('match_files')
    sub_cmd.add_argument('-p', '--path', type=str, required=True)
    sub_cmd.add_argument('-f', '--file', type=str, required=True)
    sub_cmd.add_argument('-o', '--out_file', type=str, required=False)
    sub_cmd.add_argument('-m', '--mode', type=str, required=False)
    # group by ext
    sub_cmd = sub_parser.add_parser('group_by_ext')
    sub_cmd.add_argument('-p', '--path', type=str, required=True)
    sub_cmd.add_argument('-o', '--out_file', type=str, required=False)

    args = parser.parse_args()
    if args.command in cmd_dict:
        command = args.command
        args_dict = args.__dict__.copy()
        args_dict.pop('command')
        out_file = args_dict.pop('out_file')
        out_file = out_file.strip('"').strip("'") if out_file else out_file

        for k, v in args_dict.items():
            if isinstance(v, str):
                args_dict[k] = v.strip('"').strip("'")

        result = cmd_dict[args.command](**args_dict)
        if command in ['list_all_files', 'list_all_folders']:
            print_to_stream(result, out_file)
        elif command in ['count']:
            lines = [f'{path} {n_d} {n_f}' for path, n_d, n_f in result]
            lines = ['path n_folders n_files'] + lines
            print_to_stream(lines, out_file)
        elif command in ['tree']:
            print_to_stream(tree_to_strs(result), out_file)
        elif command in ['size']:
            lines = [f'{path} {s}B' for path, s in result]
            lines = ['path size/B'] + lines
            print_to_stream(lines, out_file)
        elif command in ['group_by_ext']:
            lines = []
            for k, v in result.items():
                lines.append(k)
                lines.extend(v)
            print_to_stream(lines, out_file)
        else:
            print_to_stream(result, out_file)
    else:
        raise ValueError(f'{args.command} is not support!')


if __name__ == '__main__':
    main()
