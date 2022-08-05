from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class DelCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        fpath = [Config.netdctl_path] \
            if not self._args.a else [Config.netdctl_path, Config.networkd_path]

        file_type = None
        iface = None

        match self._args.d:
            case 'link':
                iface = self._args.src
                file_type = Config.link_ext
            case 'net':
                iface = self._args.iface
                file_type = Config.net_ext

        self._delete(fpath, file_type, iface)


    def _delete(self, file_path: list, file_type: list, iface: str):
        Helpers.delete_config(
                        file_path, 
                        iface,
                        ext=file_type
                    )        
