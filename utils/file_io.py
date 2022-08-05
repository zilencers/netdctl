import os
import sys
import shutil


class FileIO:

    @staticmethod
    def copy(src: str, dest: str):
        try:
            shutil.copy2(src, dest)
        except OSError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    
    @staticmethod
    def join(path1: str, path2: str):
        return os.path.join(path1, path2)


    @staticmethod
    def readlines(file_path: str):
        if file_path is None:
            raise Exception("path cannot be None")

        data = None
        with open(file_path, 'r') as fh:
            data = fh.readlines()

        return data


    @staticmethod
    def read(file_path: str):
        if file_path is None:
            raise Exception("path cannot be None")

        data = None
        with open(file_path, 'r') as fh:
            data = fh.readline()

        return data


    @staticmethod
    def write(file_path: str, data=[], mode='a'):
        if file_path is None: 
            raise Exception("path cannot be None")

        with open(file_path, mode) as fh:
            for d in data:
                fh.write(d)


    @staticmethod
    def file_exists(file_path: str):
        if file_path is None:
            raise Exception("path cannot be None")

        return os.path.exists(file_path)


    @staticmethod
    def dir_exists(dir_path: str, create=False):
        if os.path.exists(dir_path):
            return True

        if not os.path.exists(dir_path) and create:
            try:
                os.mkdir(dir_path)
                return True
            except OSError as e:
                print(e, file=sys.stderr)
                sys.exit(1)

        return False


    @staticmethod
    def remove_dir(dir_path: str):
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print(e, file=sys.stderr)
            sys.exit(1)


    @staticmethod
    def files_by_type(file_path: str, append_path=False, ext=''):
        if file_path is None:
            raise ValueError('file_path cannot be None')
        
        files = []
        for x in os.listdir(file_path):
            if x.endswith(ext) and append_path:
                files.append(os.path.join(file_path, x))
            elif x.endswith(ext) and not append_path:
                files.append(x)

        return files


    @staticmethod
    def get_files(file_path: str):
        if file_path is None:
            raise ValueError('file_path cannot be None')

        return os.listdir(file_path)
