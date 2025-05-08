# I do not use sets or dictionaries here because they're not necessary
# the number of commands is not expected to be large

class CommandInfo:
    def __init__(self, primary_name: str, short_name: str, alt_names: set[str] = None, descr: str = ""):
        self.primary_name = primary_name
        self.short_name = short_name
        self.alt_names = [short_name] + (alt_names or [])
        self.all_names = [primary_name] + self.alt_names
        self.descr = descr

    def help(self) -> str:
        return f"{' | '.join(self.all_names)} {self.descr}"


class ProgramInfo:
    def __init__(self, *commands: CommandInfo, foreword: str = "", postword: str = ""):
        self.foreword = foreword
        self.commands = commands
        self.postword = postword

    def get_command_info(self, command_name: str) -> CommandInfo | None:
        return next(
            (
                command for command in self.commands
                if command_name in command.all_names
            ),
            None
        )

    def help(self, command_name: str | None) -> str:
        if command_name is not None:
            command_info = self.get_command_info(command_name)
            if command_info is None:
                return None

            return command_info.help()

        column_names = ["command", "alternatively"]
        spaces = 2
        spacing = " " * spaces

        width = max(
            [len(column_names[0])] + [
                len(command.primary_name) for command in self.commands
            ]
        ) + spaces

        column_heads = f"{column_names[0].rjust(width)}{spacing}{column_names[1]}"
        command_list = "\n".join([
            f"{command.primary_name.rjust(width)}{spacing}{','.join(command.alt_names)}"
            for command in self.commands
        ])

        return "\n".join([
            self.foreword,
            column_heads,
            command_list,
            self.postword,
        ])

