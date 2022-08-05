from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class ShowCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        match self._args.s:
            case 'link':
                self._link_show()
            case 'net':
                self._net_show()


    def _link_show(self):
        Helpers.run(
            ['networkctl', 'list'],
            shell=True,
            text=False, 
            cap_output=False,
            check=True
        )


    def _net_show(self):
        fields = ['Name', 'Address', 'Gateway', 'DNS']
        data = Helpers.parse(
                         Config.networkd_path,
                         fields,
                         ext=Config.net_ext,
                    )

        headers = ['LINK', 'ADDRESS', 'GATEWAY', 'DNS']
        Helpers.display(data, headers)