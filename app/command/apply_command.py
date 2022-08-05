from app.command.icommand import ICommand
from utils.helpers import Helpers
from utils.config import Config


class ApplyCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        self.apply_now()


    def apply_now(self):
        Helpers.move_config(Config.netdctl_path, 
                            Config.networkd_path)
        #Helpers.run(Config.net('stop'))
        #Helpers.run(Config.net('start'))