from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class NetCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        tpl_name = Config.tpl_static

        if self._args.dhcp:
            tpl_name = Config.tpl_dhcp
        
        self._net_add(tpl_name)


    def _net_add(self, template: str):
        fname = self._get_filename(Config.net_ext, self._args.iface)
        self._write(fname, template)


    def _get_filename(self, ext: str, iface: str):
        return Helpers.gen_filename(
                    [Config.networkd_path,
                     Config.netdctl_path],
                     Config.prefix_spacing,
                     ext,
                     iface
                )


    def _write(self, fname: str, template: str):
        Helpers.write_config(
                        Config.netdctl_path,
                        fname, 
                        Config.template_path,
                        template,
                        **vars(self._args)
                    )