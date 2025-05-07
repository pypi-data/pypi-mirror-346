from pathlib import Path as PathWrapper
import tempfile, shutil
import os, stat
from typing import Optional


class FsysNode:
    def __init__(self, path : str):
        self._path_wrapper : PathWrapper = PathWrapper(path)

    def get_zip(self) -> bytes:
        with tempfile.TemporaryDirectory() as write_dir:
            zip_base_path = os.path.join(write_dir, 'zipfile')
            args_dir = {
                'base_name': zip_base_path,
                'format': 'zip',
            }
            if self._path_wrapper.is_file():
                args_dir['root_dir'] = self.get_parent_dirpath()
                args_dir['base_dir'] = self.get_name()

            if self._path_wrapper.is_dir():
                args_dir['root_dir'] = self.get_path()

            shutil.make_archive(**args_dir)
            with open(f'{zip_base_path}.zip', 'rb') as file:
                zip_bytes = file.read()

        return zip_bytes

    # -------------------------------------------
    # attributes

    def get_path(self) -> str:
        return str(self._path_wrapper.absolute())

    def get_parent_dirpath(self) -> str:
        return str(self._path_wrapper.parent.absolute())

    def get_name(self) -> str:
        return self._path_wrapper.name

    def is_hidden(self) -> bool:
        if os.name == 'posix':
            return os.path.basename(self.get_path()).startswith('.')
        elif os.name == 'nt':
            return bool(os.stat(self.get_path()).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        else:
            raise NotImplementedError(f'Unsupported OS: {os.name}, {FsysNode.is_hidden.__name__} is only supported '
                                      f'on Windows and Unix systems')

    def get_last_modified_epochtime(self) -> float:
        return os.path.getmtime(self.get_path())

    def get_size_in_MB(self) -> float:
        return os.path.getsize(self.get_path()) / (1024 * 1024)


class Directory(FsysNode):
    def __init__(self, path : str):
        super().__init__(path=path)
        if not self._path_wrapper.is_dir():
            raise FileNotFoundError(f'Path {path} is not a directory')

    def get_tree(self, include_root : bool = False) -> str:
        fpaths = self.get_all_subpaths(absolute=include_root)
        structure_dict = self.to_dict(fpaths)
        return self.dict_to_tree(fs_dict=structure_dict)

    def get_subfile_fpaths(self, absolute : bool = True) -> list[str]:
        subfile_paths = []
        for root, dirs, files in os.walk(self.get_path()):
            for file in files:
                fpath = os.path.join(root, file)
                subfile_paths.append(fpath)
        if not absolute:
            subfile_paths = [os.path.relpath(p, self.get_path()) for p in subfile_paths]
        return subfile_paths

    def get_all_subpaths(self, absolute : bool = True) -> list[str]:
        all_paths = []
        for root, dirs, files in os.walk(self.get_path()):
            for d in dirs:
                dirpath = os.path.join(root, d)
                all_paths.append(dirpath)
            for f in files:
                fpath = os.path.join(root, f)
                all_paths.append(fpath)
        if not absolute:
            all_paths = [os.path.relpath(p, self.get_path()) for p in all_paths]

        return all_paths

    @classmethod
    def dict_to_tree(cls, fs_dict: dict, indent: int = 0, parent_dirpath : str = '', max_children: int = 10) -> str:
        total_str = ''
        if not fs_dict:
            return total_str

        items = fs_dict.items()
        for n, (k, v) in enumerate(items):
            indentation = '\t' * indent

            if n == max_children:
                total_str += f'{indentation}... (Max folder elements displayed = {max_children})\n'
                break

            parent_name = os.path.basename(parent_dirpath)
            parent_indicator = f'-> {parent_name}/' if parent_name else ''

            fpath = os.path.join(parent_dirpath, k)
            is_file = os.path.isfile(fpath)
            symbol = f'🗎' if is_file else '🗀'
            conditional_backslash = '' if is_file else '/'
            total_str += (f'{indentation}{symbol} {k}{conditional_backslash} {parent_indicator}\n'
                          f'{cls.dict_to_tree(v, indent=indent + 1, parent_dirpath=fpath)}')
        if indent == 0:
            total_str = total_str.rstrip()
        return total_str

    @staticmethod
    def to_dict(fpaths: list[str]) -> dict:
        tree_dict = {}
        for path in fpaths:
            parts = path.split('/')
            node = tree_dict
            for p in parts:
                if not p in node:
                    node[p] = {}
                node = node[p]
        return tree_dict

class File(FsysNode):
    def __init__(self, path : str):
        super().__init__(path=path)
        if not self._path_wrapper.is_file():
            raise FileNotFoundError(f'Path {path} is not a file')

    def get_suffix(self) -> Optional[str]:
        parts = self.get_name().split('.')
        if len(parts) == 1:
            return None
        else:
            return parts[-1]


if __name__ == "__main__":
    directory = Directory(path='/home/daniel/misc/holytools', )
    print(directory.get_tree())