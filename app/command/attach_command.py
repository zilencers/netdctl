from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class AttachCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        self._attach()


    def _attach(self):
        fname = self._get_filename(Config.net_ext, self._args.iface)
        updated_args = self._update_args()
        self._write(fname, Config.tpl_attach, updated_args)


    def _update_args(self):
        """ Check for multiple vlan names and update args """

        args = vars(self._args)
        
        if self._args.name is not None:
            values = self._args.name.split(',')
            if len(values) > 1:
                i = 0
                for v in values:
                    k = 'name' + str(i)
                    args.update({k: v})
                    i += 1

        return args


    def _get_filename(self, ext: str, iface: str):
        return Helpers.gen_filename(
                    [Config.networkd_path,
                     Config.netdctl_path],
                     Config.prefix_spacing,
                     ext,
                     iface
                )


    def _write(self, fname: str, template: str, args: dict):
        Helpers.write_config(
                        Config.netdctl_path,
                        fname, 
                        Config.template_path,
                        template,
                        **args
                    )