import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.exceptions as exceptions
import pdfriend.classes.cmdparsers as cmdparsers
import pdfriend.classes.shells as shells
import pdfriend.classes.info as info
from pdfriend.ops.pdf import rotate
from pdfriend.classes.platforms import Platform
from pdfriend.classes.config import Config
import pdfriend.utils as utils
import pathlib


program_info = info.ProgramInfo(
    info.CommandInfo("help", "h", descr = """[command?]
    display help message. If given a command, it will only display the help message for that command.

    examples:
        help rotate
            displays the help blurb for the rotate command
        help exit
            displays the help blurb for the exit command
    """),
    info.CommandInfo("exit", "e", descr = """
    exits the edit mode
    """),
    info.CommandInfo("rotate", "r", descr = """[page_numbers] [angle]
    rotates page clockwise with the given numbers (starting from 1) by the given angle (in degrees). Can use negative angles to rotate counter-clockwise. DO NOT put extra spaces between the page numbers!

    examples:
        r 34 1.2
            rotates page 34 clockwise by 1.2 degrees
        r 1,3,8 -4
            rotates pages 1,3 and 8 counter-clockwise by 4 degrees
        r 3:18 90
            rotates pages 3 through 18 (INCLUDING 18) clockwise by 90 degrees
        r 1,13,5:7,2 54
            rotates pages 1,2,5,6,7,13 clockwise by 54 degrees
        r all -90
            rotates all pages counter-clockwise by 90 degrees
    """),
    info.CommandInfo("delete", "d", descr = """[page_numbers]
    deletes all specified pages. DO NOT put extra spaces between the page numbers!

    examples:
        d 7
            deletes page 7
        d 4,8,1
            deletes pages 1, 4 and 8
        d 6:66
            deletes pages 6 through 66 (INCLUDING 66)
        d :13
            deletes all pages up to and including 13
        d 4,17,3:6
            deletes pages 3,4,5,6 and 17
    """),
    info.CommandInfo("swap", "s", descr = """[page_0] [page_1]
    swaps page_0 and page_1.
    """),
    info.CommandInfo("move", "m", descr = """[source] [destination]
    move source to BEFORE destination, taking its place.

    examples:
        m 3 17
            moves page 3 to page 17, pushing back the pages from 17 onward
        m 83 1
            moves page 83 to the beginning of the document
    """),
    info.CommandInfo("push", "p", descr = """[pages] [offset]
    pushes the specified pages by offset pages (offset can be negative).

    examples:
        p 3 7
            moves page 3 to 7 pages down, i.e. to page 10.
        p 4,9,2 1
            moves pages 2,4,9 by 1 page.
        p 5:8 -3
            moves pages 5,6,7,8 to 3 pages BACK.
        p 5,6,90:94 5
            moves pages 5,6,90,91,92,93,94 to be 5 pages down.
        p :5 4
            moves pages 1,2,3,4,5 to be 4 pages down.
        p 67: -7
            move pages from 67 to the end of the PDF to be 7 pages back.
        p 70: 5
            FAILS. 70: includes the end of the PDF, and you can't move that further down.
    """),
    info.CommandInfo("undo", "u", descr = """[number?]
    undo the previous [number] commands.

    examples:
        u
            undoes the previous command
        u 3
            undoes the previous 3 commands
        u all
            undoes all commands issued this session (reverts document fully)
    """),
    info.CommandInfo("export", "x", descr = """[filename?=pdfriend_edit.txt]
    exports all the commands you ran into a text file

        examples:
            x
                exports your commands to pdfriend_edit.txt
            x out.txt
                exports your commands to out.txt
    """),
    foreword = "pdfriend edit shell for quick changes. Commands:",
    postword = "use h [command] to learn more about a specific command"
)


class EditRunner(shells.ShellRunner):
    def __init__(self, pdf: wrappers.PDFWrapper, open_pdf: bool = True):
        backup_path = pdf.backup()
        print(f"editing {pdf.source}\nbackup created in {backup_path}")

        self.pdf = pdf
        self.backup_path = backup_path

        if open_pdf:
            Platform.OpenFile(pdf.source)

    def parse(self, arg_str) -> list[str]:
        return utils.parse_command_string(arg_str)

    def run(self, args: list[str]):
        cmd_parser = cmdparsers.CmdParser.FromArgs(
            program_info,
            args,
            no_command_message = "No command specified! Type h or help for a list of the available commands"
        )
        short = cmd_parser.short()

        if short == "h":
            subcommand = cmd_parser.next_str_or(None)
            print(program_info.help(subcommand))

            # this is to prevent rewriting the file and appending
            # the command to the command stack
            raise exceptions.ShellContinue()
        elif short == "e":
            raise exceptions.ShellExit()
        elif short == "r":
            pages = cmd_parser.next_pdf_slice(self.pdf, "pages")
            angle = cmd_parser.next_float("angle")

            if len(pages) == 0:
                return
            # the slice is sorted, so if any pages are out of range, it'll
            # either be the first or the last one, probably the last
            self.pdf.raise_if_out_of_range(pages[-1])
            self.pdf.raise_if_out_of_range(pages[0])

            self.pdf.pages_map_subset(rotate, pages, angle)
        elif short == "d":
            pages = cmd_parser.next_pdf_slice(self.pdf, "pages")

            for page in pages:
                self.pdf.pages_pop(page)
        elif short == "s":
            page_0 = cmd_parser.next_int("page_0")
            self.pdf.raise_if_out_of_range(page_0)
            page_1 = cmd_parser.next_int("page_1")
            self.pdf.raise_if_out_of_range(page_1)

            self.pdf.pages_swap(page_0, page_1)
        elif short == "m":
            source = cmd_parser.next_int("source")
            self.pdf.raise_if_out_of_range(source)
            destination = cmd_parser.next_int("destination")
            self.pdf.raise_if_out_of_range(destination)

            page = self.pdf.pages_pop(source - 1)
            self.pdf.pages_insert(destination - 1, page)
        elif short == "p":
            pages = cmd_parser.next_pdf_slice(self.pdf, "pages")
            offset = cmd_parser.next_int("offset")

            last_page_before = pages[-1]
            last_page_after = last_page_before + offset

            # only check last page, as the slice is sorted
            if last_page_after > self.pdf.pages_len():
                raise exceptions.ExpectedError(
                    f"can't move page {last_page_before} to {last_page_after}, as it's outside the PDF (number of pages: {self.pdf.len()})"
                )

            if offset > 0:
                pages = pages[::-1]

            for page in pages:
                p = self.pdf.pages_pop(page - 1)
                self.pdf.pages_insert(page + offset - 1, p)
        elif short == "u":
            # arg will be converted to int, unless it's "all". Defaults to 1
            num_of_commands = cmd_parser.next_typed_or(
                "int or \"all\"", lambda s: s if s == "all" else int(s),
                1  # default value
            )

            raise exceptions.ShellUndo(num_of_commands)
        elif short == "x":
            filename = cmd_parser.next_str_or("pdfriend_edit.txt")

            raise exceptions.ShellExport(filename)

    def reset(self):
        self.pdf.reread(self.backup_path)

    def save(self):
        self.pdf.write()

    def exit(self):
        pass


def edit(
    pdf: wrappers.PDFWrapper,
    commands: list[str] | None = None,
    open_pdf: bool = True
):
    edit_shell = shells.Shell(
        runner = EditRunner(pdf, open_pdf = open_pdf)
    )

    edit_shell.run(commands)
