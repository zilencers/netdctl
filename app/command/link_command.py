from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class LinkCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
                self._link_add()


    def _link_add(self):      
        fname = self._get_filename(Config.link_ext, self._args.dest)

        self._args.mac = Helpers.get_mac_addr(
                        Config.mac_path, 
                        self._args.src
                    )

        self._write(fname, Config.tpl_link)


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