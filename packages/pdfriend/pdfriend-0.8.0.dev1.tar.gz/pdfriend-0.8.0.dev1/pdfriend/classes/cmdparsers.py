import pdfriend.classes.exceptions as exceptions
import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.info as info
from pdfriend.classes.config import Config
import pathlib
import re
from typing import Self

def to_typed(input: str, type_name: str, type_converter, name: str | None = None, err_message = ""):
    try:
        return type_converter(input)
    except Exception:
        raise exceptions.ExpectedError(
            f"value \"{input}\" could not be converted to type \"{type_name}\"{err_message}"
        )

def to_file(input: str, name: str | None = None, err_message = "") -> pathlib.Path:
    file_path = pathlib.Path(input)
    if not file_path.is_file():
        raise exceptions.ExpectedError(
            f"file \"{file_path}\" was not found{err_message}"
        )

    return file_path

def to_pdf(input: str, name: str | None = None, err_message = "") -> wrappers.PDFWrapper:
    file_path = to_file(input, err_message = err_message)

    try:
        return wrappers.PDFWrapper.Read(file_path)
    except Exception as e:
        debug_message = "\nadditional info:\n{e}" if Config.Debug else ""
        raise exceptions.ExpectedError(
            f"file \"{file_path}\" could not be read as PDF{err_message}{debug_message}"
        )


def to_shell_import(input: str, name: str | None = None, err_message = "") -> list[str]:
    file = to_file(input, name = name, err_message = err_message)
    try:
        return [
            line for line in file.read_text().split("\n")
            if line != ""
        ]
    except Exception:
        raise exceptions.ExpectedError(
            f"could not read commands from file {input}{err_message}"
        )


class CmdParser:
    def __init__(self, cmd_info: str, args: list[str]):
        self.cmd_info = cmd_info
        self.args = args
        self.current_arg = 1

    def name(self) -> str:
        return self.cmd_info.primary_name

    def short(self) -> str:
        return self.cmd_info.short_name

    def arg_str(self, arg_name: str | None) -> str:
        arg_name_str = "" if arg_name is None else f" (\"{arg_name}\")"

        return f"argument {self.current_arg}{arg_name_str}"

    def loc_str(self, arg_name: str | None) -> str:
        return f"--> in {self.arg_str(arg_name)} of command \"{self.name()}\""

    @classmethod
    def FromArgs(cls,
        program_info: info.ProgramInfo,
        args: list[str],
        no_command_message: str | None = None
    ) -> Self:
        if len(args) == 0:
            raise exceptions.ExpectedError(
                no_command_message or "no command specified"
            )

        command_name = args[0]
        command_info = program_info.get_command_info(command_name)
        if command_info is None:
            raise exceptions.ExpectedError(
                f"command \"{command_name}\" does not exist"
            )

        return CmdParser(command_info, args[1:])

    @classmethod
    def FromString(cls,
        program_info: info.ProgramInfo,
        string: str,
        no_command_message: str | None = None
    ) -> Self:
        whitespace_pattern = re.compile(r"\s+")

        return cls.FromArgs(
            program_info,
            re.split(whitespace_pattern, string),
            no_command_message = no_command_message
        )

    def ensure_next_exists(self, name: str | None = None):
        if len(self.args) == 0:
            raise exceptions.ExpectedError(
                f"{self.arg_str(name)} for command \"{self.name()}\" not provided"
            )

    def advance(self, head, tail):
        self.args = tail
        self.current_arg += 1
        return head

    def split_head(self, name: str | None = None):
        self.ensure_next_exists(name = name)

        return (self.args[0], self.args[1:])

    def next_str(self, name: str | None = None):
        head, tail = self.split_head(name = name)

        return self.advance(head, tail)

    def next_str_or(self, default: str, name: str | None = None) -> str:
        try:
            return self.next_str(name)
        except Exception:
            return default

    def next_typed(self, type_name: str, type_converter, name: str | None = None):
        head, tail = self.split_head(name = name)

        return self.advance(
            to_typed(
                head, type_name, type_converter,
                name = name,
                err_message = f"\n{self.loc_str(name)}"
            ),
            tail
        )

    def next_typed_or(self, type_name: str, type_converter, default, name: str | None = None):
        try:
            return self.next_typed(type_name, type_converter, name)
        except Exception:
            return default

    def next_int(self, name: str | None = None) -> int:
        return self.next_typed("int", int, name)

    def next_int_or(self, default: int, name: str | None = None) -> int:
        try:
            return self.next_int(name)
        except Exception:
            return default

    def next_float(self, name: str | None = None) -> float:
        return self.next_typed("float", float, name = name)

    def next_float_or(self, default: float, name: str | None = None) -> float:
        try:
            return self.next_float(name = name)
        except Exception:
            return default

    def next_pdf_slice(self, pdf: wrappers.PDFWrapper, name: str | None = None) -> list[int]:
        return self.next_typed("PDF slice", lambda s: pdf.pages_view(s), name = name)

    def next_pdf_slice_or(self, pdf: wrappers.PDFWrapper, default: list[int], name: str | None = None) -> list[int]:
        try:
            return self.next_pdf_slice(pdf, name = name)
        except Exception:
            return default

    def next_file(self, name: str | None = None) -> pathlib.Path:
        head, tail = self.split_head(name = name)

        return self.advance(
            to_file(head, name, err_message = f"\n{self.loc_str(name)}"),
            tail
        )

    def next_file_or(self, default: pathlib.Path, name: str | None = None) -> pathlib.Path:
        try:
            return self.next_file(name = name)
        except Exception:
            return default

    def next_pdf(self, name: str | None = None) -> wrappers.PDFWrapper:
        head, tail = self.split_head(name = name)

        return self.advance(
            to_pdf(head, name, err_message = f"\n{self.loc_str(name)}"),
            tail
        )

    def next_pdf_or(self, default: wrappers.PDFWrapper, name: str | None = None) -> wrappers.PDFWrapper:
        try:
            return self.next_pdf(name = name)
        except Exception:
            return default

