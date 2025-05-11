import os
import sys
import traceback
from typing import Callable, Optional

from petcmd.argparser import ArgParser
from petcmd.command import Command
from petcmd.exceptions import CommandException
from petcmd.interface import Interface
from petcmd.utils import validate_type_hints, get_signature

class Commander:

	def __init__(self, error_handler: Callable[[Exception], None] = None, compact_commands_list: bool = False):
		self.__error_handler = error_handler
		self.__commands: list[Command] = []
		self.__compact_commands_list = compact_commands_list
		self.__completion_commands = ["show-shell-completion", "setup-shell-completion",
			"remove-shell-completion", "setup-zshrc-for-completion", "help-completion"]

		@self.command("help")
		def help_command(command: str = None):
			"""
			Show a help message or usage message when a command is specified.

			:param command: Command for which instructions for use will be displayed.
			"""
			self.__help_command(command)

		@self.command("help-completion")
		def help_completion():
			"""Show a help message for completion commands."""
			Interface.commands_list([c for c in self.__commands if c.cmds[0] in self.__completion_commands])

		@self.command("show-shell-completion")
		def show_shell_completion(alias: str = None):
			"""
			Print a shell completion script for the current cli tool.

			:param alias:   Alias for the cli tool completion.
							If not specified, the name of the current script is used.
			"""
			if alias is None:
				alias = os.path.basename(sys.argv[0])
			print(self.__generate_completion(alias))

		@self.command("setup-shell-completion")
		def setup_shell_completion(alias: str = None):
			"""
			Set up a shell completion script for the current cli tool.
			Save it to ~/.zsh/completions/_alias.

			:param alias:   Alias for the cli tool completion.
							If not specified, the name of the current script is used.
			"""
			if alias is None:
				alias = os.path.basename(sys.argv[0])
			completions = os.path.join(os.path.expanduser("~"), ".zsh", "completions")
			os.makedirs(completions, exist_ok=True)
			with open(os.path.join(completions, f"_{alias}"), "w") as f:
				f.write(self.__generate_completion(alias))
			print(f"Shell completion script for {alias} has been saved to {completions}. Restart terminal to load it.")

		@self.command("remove-shell-completion")
		def remove_shell_completion(alias: str = None):
			"""
			Remove a shell completion script for the current cli tool.
			Search it in ~/.zsh/completions/_alias.

			:param alias:   Alias for the cli tool completion.
							If not specified, the name of the current script is used.
			"""
			os.remove(os.path.join(os.path.expanduser("~"), ".zsh", "completions", f"_{alias}"))

		@self.command("setup-zshrc-for-completion")
		def setup_zshrc_for_completion():
			"""Fill ~/.zshrc with commands to enable shell completion for zsh with ~/.zsh/completions/* files."""
			home = os.path.expanduser("~")
			zshrc = os.path.join(home, ".zshrc")
			completions = os.path.join(home, ".zsh", "completions")
			if not os.path.exists(zshrc):
				with open(zshrc, "w") as f:
					f.write("")
			with open(zshrc, "r") as f:
				content = f.read()
			commands = [
				f"fpath=({completions} $fpath)",
				"autoload -Uz compinit",
				"compinit"
			]
			with open(zshrc, "a") as f:
				if any(command not in content for command in commands):
					f.write("\n")
				for command in commands:
					if command not in content:
						f.write(f"{command}\n")

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
		Interface.commands_list([c for c in self.__commands if c.cmds[0] not in self.__completion_commands],
			self.__compact_commands_list)

	# noinspection PyListCreation
	def __generate_completion(self, alias: str):
		script = []
		script.append(f"#compdef {alias}")
		script.append("")

		script.append("_arguments -C \\")
		script.append(f"  '1:command:({" ".join(" ".join(c.cmds) for c in self.__commands)})' \\")
		script.append("  '*::args:->args'")
		script.append("")

		script.append("case $words[1] in")
		for command in self.__commands:
			for command_name in command.cmds:
				script.append(f"  {command_name})")
				script.append("    _arguments \\")
				positionals, keyword, *_ = get_signature(command.func)
				for arg in [*positionals, *keyword]:
					arg = arg.replace('_', '-')
					script.append(f"      '--{arg}::' \\")
				script.append("    ;;")
		script.append("esac")
		script.append("")

		return "\n".join(script)
