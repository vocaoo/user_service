from abc import ABC

from didiator import Command as DCommand, CommandHandler as DCommandHandler


class Command[CRes](DCommand[CRes], ABC):
    pass


class CommandHandler[C: Command, CRes](DCommandHandler[C, CRes], ABC):
    pass
