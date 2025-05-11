
import sys
import traceback
from typing import Callable, Optional

from petcmd.argparser import ArgParser
from petcmd.command import Command
from petcmd.exceptions import CommandException
from petcmd.interface import Interface
from petcmd.utils import validate_type_hints

class Commander:

	def __init__(self, error_handler: Callable[[Exception], None] = None, compact_commands_list: bool = False):
		self.__error_handler = error_handler
		self.__commands: list[Command] = []
		self.__compact_commands_list = compact_commands_list

		@self.command("help")
		def help_command(command: str = None):
			"""
			Show a help message or usage message when a command is specified.
			:param command: Command for which instructions for use will be displayed.
			"""
			self.__help_command(command)

	def command(self, *cmds: str):
		def dec(func: Callable) -> Callable:
			for command in self.__commands:
				if command.match(cmds):
					raise CommandException(f"Duplicated command: {", ".join(cmds)}")
			validate_type_hints(func)
			self.__commands.append(Command(cmds, func))
			return func
		return dec

	def process(self, argv: list[str] = None):
		if argv is None:
			argv = sys.argv[1:]
		command = self.__find_command(argv[0] if len(argv) > 0 else "help")
		if command is None:
			print(f"\nUnknown command '{argv[0]}'")
			self.__help_command()
			return
		try:
			args, kwargs = ArgParser.parse(argv[1:], command)
			command.func(*args, **kwargs)
		except CommandException as e:
			print("\n" + str(e))
			Interface.command_usage(command)
		except Exception as e:
			print("\n" + traceback.format_exc())
			if isinstance(self.__error_handler, Callable):
				self.__error_handler(e)

	def __find_command(self, cmd: str) -> Optional[Command]:
		for command in self.__commands:
			if command.match(cmd):
				return command

	def __help_command(self, cmd: str = None):
		if cmd is not None:
			command = self.__find_command(cmd)
			if command and command.match(cmd):
				Interface.command_usage(command)
				return
		Interface.commands_list(self.__commands, self.__compact_commands_list)
