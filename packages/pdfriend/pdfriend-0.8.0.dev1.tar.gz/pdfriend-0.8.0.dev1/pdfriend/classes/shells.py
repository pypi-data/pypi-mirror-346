import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.exceptions as exceptions
import pdfriend.utils as utils
from pdfriend.classes.config import Config
from abc import ABC, abstractmethod

def input_generator():
    while True:
        yield input("")


class ShellRunner(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def parse(self, arg_str: str) -> list[str]:
        pass

    @abstractmethod
    def run(self, args: list[str]):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def exit(self):
        pass


class Shell:
    def __init__(self, runner: ShellRunner):
        self.command_stack = []
        self.runner = runner

    def run_command(self, args: list[str]):
        args = self.runner.parse(args)
        self.runner.run(args)
        self.command_stack.append(args)
        self.runner.save()

    def undo(self, num_of_commands: int | str):
        if num_of_commands == "all":
            self.command_stack = []
        else:
            self.command_stack = self.command_stack[:-num_of_commands]

        self.runner.reset()
        for args in self.command_stack:
            self.runner.run(args)

        self.runner.save()

    def export(self, filename: str):
        with open(filename, "w") as outfile:
            outfile.write("\n".join([
                " ".join(args) for args in self.command_stack
            ]))

    def run_commands(self, commands: list[str]):
        for arg_str in commands:
            try:
                self.run_command(arg_str)
            except (KeyboardInterrupt, exceptions.ShellExit):
                self.runner.exit()
                return
            except exceptions.ShellContinue:
                continue
            except exceptions.ShellUndo as undo:
                self.undo(undo.num)
                # pdf.reread(backup_path)
            except exceptions.ShellExport as export:
                self.export(export.filename)
            except exceptions.ExpectedError as e:
                print(e)
            except Exception as e:
                utils.print_unexpected_exception(e, Config.Debug)

    def run(self, commands: list[str] | None = None):
        if commands is None:
            commands = input_generator()

        self.run_commands(commands)
