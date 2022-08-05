from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class UpdateCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        match self._args.u:
            case 'link':
                pass
            case 'net':
                self._net_update()


    def _net_update(self):
        search_paths = [
                        Config.netdctl_path, 
                        Config.networkd_path
                    ]
        
        net_map = {'addr': 'Address', 'dns': 'DNS', 'gw': 'Gateway'}
        Helpers.update_config(
            search_paths,
            Config.net_ext,
            net_map,
            **vars(self._args)
        )