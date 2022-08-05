from app.command.icommand import ICommand
from utils.helpers import Helpers


class ReloadCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        Helpers.run(['networkctl', 'reload'], True)