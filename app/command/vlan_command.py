from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class VlanCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        self._vlan_add()


    def _vlan_add(self):
        fname = self._get_filename(Config.vlan_ext)
        self._write(fname, Config.tpl_vlan)


    def _get_filename(self, ext: str):
        return Helpers.gen_filename(
                    [Config.networkd_path,
                     Config.netdctl_path],
                     Config.prefix_spacing,
                     ext,
                     self._args.name
                )


    def _write(self, fname: str, template: str):
        Helpers.write_config(
                        Config.netdctl_path,
                        fname, 
                        Config.template_path,
                        template,
                        **vars(self._args)
                    )