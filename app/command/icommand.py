from abc import ABCMeta, abstractstaticmethod


class ICommand(metaclass=ABCMeta):

    @abstractstaticmethod
    def execute():
        """A static interface method"""