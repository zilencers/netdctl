import os
import sys
from zipfile import ZipFile

from app.command.icommand import ICommand
from utils.file_io import FileIO
from utils.config import Config


class ImportCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        self._import()


    def _import(self):
        """ A method for importing configuration """

        if self._is_zip(self._args.file):
            self._extract(self._args.file, Config.networkd_path)
        else:
            self._is_cfgfile(self._args.file)


    def _is_cfgfile(self, file: str):
        """ A method for checking for a valid networkd file extension """

        ext = os.path.basename(file).split('.')
        valid_ext = [Config.link_ext, Config.net_ext, Config.vlan_ext]

        if not ext in valid_ext:
            print("Invalid config extension: {}", ext, file=sys.stderr)
            sys.exit(1)

        FileIO.copy(file, Config.netdctl_path)


    def _is_zip(self, file: str):
        """ A method for checking for a valid zip file """

        return ZipFile.is_zipfile(file)


    def _extract(self, arcname: str, path='.'):
        """ A method for extracting archived network configuration """

        zip = ZipFile(arcname)
        zip.extractall(path)
        zip.close()