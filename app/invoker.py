from app.command.apply_command import ApplyCommand
from app.command.attach_command import AttachCommand
from app.command.archive_command import ArchiveCommand
from app.command.bridge_command import BridgeCommand
from app.command.del_command import DelCommand
from app.command.import_command import ImportCommand
from app.command.link_command import LinkCommand
from app.command.net_command import NetCommand
from app.command.reload_command import ReloadCommand
from app.command.show_command import ShowCommand
from app.command.update_command import UpdateCommand
from app.command.vlan_command import VlanCommand


class Invoker:
    def __init__(self, args):
        self._args = args
        self._commands = {}


    def register(self, command_name: str):
        self._commands[command_name] = globals()[command_name](self._args)


    def execute(self, command_name: str):
        if command_name in self._commands:
            self._commands[command_name].execute()
            