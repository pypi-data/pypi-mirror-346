
from types import GenericAlias
from typing import Callable, Iterable

from petcmd.utils import get_signature, FilePath
from petcmd.command import Command

class ZshAutocompletion:

	# noinspection PyListCreation
	@classmethod
	def generate(cls, commands: list[Command], alias: str) -> str:
		script = []
		script.append(f"#compdef {alias}")
		script.append("")

		script.append("_arguments -C \\")
		script.append(f"  '1:command:({" ".join(" ".join(c.cmds) for c in commands)})' \\")
		script.append("  '*::args:->args'")
		script.append("")

		script.append("case $words[1] in")
		for command in commands:
			for command_name in command.cmds:
				script.append(f"  {command_name})")
				script.append("    _arguments \\")
				positionals, keyword, defaults, spec = get_signature(command.func)
				for arg in [*positionals, *keyword]:
					param = arg.replace('_', '-')
					typehint = spec.annotations.get(arg)
					if isinstance(typehint, GenericAlias):
						typehint = typehint.__origin__
					if command.shell_complete and command.shell_complete.get(arg) is not None:
						values = command.shell_complete[arg]
						if isinstance(values, Callable):
							script.append(cls.default_value_param(param, values()))
						elif isinstance(values, (list, dict, str)):
							script.append(cls.default_value_param(param, values))
						else:
							script.append(cls.value_param(param))
					elif typehint == bool:
						if arg not in positionals and defaults.get(arg) is False:
							script.append(cls.no_value_param(param))
						else:
							script.append(cls.default_value_param(param, ["0", "false", "1", "true"]))
					elif typehint == FilePath:
						script.append(cls.path_value_param(param, ))
					else:
						script.append(cls.value_param(param))
				script.append("    ;;")
		script.append("esac")
		script.append("")

		return "\n".join(script)

	@classmethod
	def value_param(cls, arg: str) -> str:
		return f"      '--{arg}::' \\"

	@classmethod
	def no_value_param(cls, arg: str) -> str:
		return f"      '--{arg}' \\"

	@classmethod
	def default_value_param(cls, arg: str, values: Iterable | str) -> str:
		if not isinstance(values, str):
			values = " ".join(f'"{value}"' for value in values)
		return f"      '--{arg}:{arg}:({values})' \\"

	@classmethod
	def path_value_param(cls, arg: str) -> str:
		return f"      '--{arg}:{arg}:_files' \\"



