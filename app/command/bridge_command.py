from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class BridgeCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        self._bridge_add()


    def _bridge_add(self):
        fname = self._get_filename()
        self._write(fname)


    def _get_filename(self):
        return Helpers.gen_filename(
                    [Config.networkd_path,
                     Config.netdctl_path],
                     Config.prefix_spacing,
                     Config.bridge_ext,
                     self._args.iface
                )


    def _write(self, fname: str):
        Helpers.write_config(
                        Config.netdctl_path,
                        fname, 
                        Config.template_path,
                        Config.tpl_bridge,
                        **vars(self._args)
                    )