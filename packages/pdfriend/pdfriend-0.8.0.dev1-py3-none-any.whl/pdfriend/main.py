import argparse
import traceback
from pdfriend.classes.config import Config
from pdfriend.classes.platforms import Platform
import pdfriend.classes.cmdparsers as cmdparsers
import pdfriend.classes.exceptions as exceptions
import pdfriend.classes.info as info
import pdfriend.commands as commands
import pdfriend.utils as utils


program_info = info.ProgramInfo(
    info.CommandInfo("version", "v", descr = """ | -v | --version
    prints the current version of pdfriend
    """),
    info.CommandInfo("help", "h", descr = """ [command?]
        display help message. If given a command, it will only display the help message for that command.

        examples:
            pdfriend help merge
                prints out the help blurb for the merge command
            pdfriend help
                prints out generic help message, with a command list
    """),
    info.CommandInfo("merge", "m", descr = """ [filename1] [filename2?] ... [-o|--outfile outfile?=pdfriend_output.pdf] [-q|--quality quality?=100]
        merge the given files into one pdf. It can handle multiple pdfs, as well convert and merge png and jpg images. Glob patterns are also supported. You can specify the output filename using the -o or --outfile flag, otherwise it defaults to pdfriend_output.pdf. You can also specify the quality when images are converted to pdfs via the -q or --quality flag. It's an integer going from 0 to 100, 100 is no lossy compression and 0 is full lossy compression.

    examples:
        pdfriend merge pdf1.pdf img.png pdf2.pdf -o merged.pdf
            merges all of those into merged.pdf, preserving the quality of img.png
        pdfriend merge folder_name/* -o merged.pdf -q 50
            merges all files in directory folder_name into merged.pdf and compresses the images by 50%.
        pdfriend merge pdf1.pdf folder_name/* img.jpg pdf2.pdf -o apricot.pdf
            merges every file given, including all files in folder_name, into apricot.pdf
    """),
    info.CommandInfo("split", "s", descr = """ [filename] [pages] ... [-o|--outfile outfile?=pdfriend_output]
        split the given file at the given points. Every point is included in the part after, not before it.

        examples:
            pdfriend split in.pdf 5 -o parts
                splits in.pdf into one part with pages 1-4 and another with 5-end and puts them in a directory named parts
            pdfriend split input.pdf 4,7
                splits input.pdf into 3 parts, one has pages 1-3, another 4-6 and another 7-end and puts them in a directory named pdfriend_output
            pdfriend split thing.pdf 8:11
                splits thing.pdf into 4 parts, one has pages 1-7, another has page 8, the other page 9, the other page 10, and the other pages 11-end and puts them in a directory named pdfriend_output
            pdfriend split infile.pdf all -o pages
                splits infile.pdf into individual pages and puts them in a directory named pages
    examples:
        pdfriend merge pdf1.pdf img.png pdf2.pdf -o merged.pdf
            merges all of those into merged.pdf, preserving the quality of img.png
        pdfriend merge folder_name/* -o merged.pdf -q 50
            merges all files in directory folder_name into merged.pdf and compresses the images by 50%.
        pdfriend merge pdf1.pdf folder_name/* img.jpg pdf2.pdf -o apricot.pdf
            merges every file given, including all files in folder_name, into apricot.pdf
    """),
    info.CommandInfo("edit", "e", descr = """ [filename] [-I|--import command_file?]
        edit the selected file in place, using a set of subcommands. After launching the edit shell, you can type h or help to list the subcommands. You can import pdfriend edit subcommands from text files using -I. The text files must have the edit subcommands as you would write them on the shell, separated by newlines. Try running some commands in the edit shell and then exporting them using the x command.

        examples:
            pdfriend edit notes.pdf
                launches the edit shell on notes.pdf
            pdfriend edit fried.pdf -I some_commands.txt
                executes the commands in some_commands.txt and immediately exits the edit shell
    """),
    info.CommandInfo("tinker", "t", descr = """ [filename] [-I|--import command_file?]
        edit the selected file page by page. Currently there is only the ability to show and export images

        examples:
            pdfriend tinker notes.pdf
                launches the tinker shell on notes.pdf
            pdfriend tinker fried.pdf -I some_commands.txt
                executes the commands in some_commands.txt and immediately exits the tinker shell
    """),
    info.CommandInfo("invert", "i", descr = """ [filename] [-o|--outfile outfile?=pdfriend_output.pdf] [-i|--inplace?]
        create a PDF file with the pages of the input file, but in inverted order. Adding -i or --inplace will make it so the input file is modified, instead of creating a new one.

        examples:
            pdfriend invert puppy.pdf -o puppy-inv.pdf
                inverts the pages of puppy.pdf and saves to puppy-inv.pdf
            pdfriend invert kitty.pdf -i
                inverts the pages of kitty.pdf
    """),
    info.CommandInfo("cache", "c", descr = """ [subcommand]
        for managing the pdfriend cache. Currently, you can only clear it

        examples:
            pdfriend cache clear
                clears the cache
    """),
    info.CommandInfo("weave", "w", descr = """ [filename_0] [filename_1] [-o|--outfile?=pdfriend_output.pdf]
        combines two PDFs such that the first fills the odd pages and the second the even pages of the output.

        examples:
            pdfriend weave inf0.pdf inf1.pdf
                weaves the two PDFs and saves the output to pdfriend_output.pdf
            pdfriend weave k.pdf l.pdf -o weaved.pdf
                weaves the two PDFs and saves the output to weaved.pdf
    """),
    info.CommandInfo("get", "g", descr = """ [filename] [pages] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        takes the given pages out of the PDF and puts them in the specified output file.

        examples:
            pdfriend get comic.pdf 34 -o comic-34.pdf
                gets the 34th page of comic.pdf and puts it into comic-34.pdf
            pdfriend get sth.pdf 1,2,7
                gets the pages 1,2,7 from sth.pdf and puts them into pdfriend_output.pdf
            pdfriend get reef.pdf 3:54 -o reef_main.pdf
                gets pages 3 through 54 (INCLUDING 54) and puts them into reef_main.pdf
            pdfriend get shrimp_manual.pdf 5: -o shrimp_manual_trimmed.pdf
                gets pages from 5 to the end of shrimp_manual.pdf and puts them into shrimp_manual_trimmed.pdf
            pdfriend get notes.pdf 3,4:15,18,20 -i
                gets pages 3,4,5,...,15,18,20 from notes.pdf and MODIFIES the file such that it only has those pages
    """),
    info.CommandInfo("encrypt", "n", descr = """ [filename] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        creates an encrypted PDF file using a provided password. Adding -i or --inplace will make it so that the file itself is encrypted.

        examples:
            pdfriend encrypt not-sus.pdf -i
                encrypts not-sus.pdf in-place. Make sure you remember the password, as it will be overwritten!
            pdfriend encrypt balance.pdf -o balance-encrypted.pdf
                encrypts balance.pdf and saves to balance-encrypted.pdf.
            pdfriend encrypt acct.pdf
                encrypts acct.pdf and saves to pdfriend_output.pdf.
    """),
    info.CommandInfo("decrypt", "d", descr = """ [filename] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        decrypts an encrypted PDF file using a provided password. Adding -i or --inplace will make it so that the file itself is decrypted. If the file is not encrypted, it will just be copied.

        examples:
            pdfriend decrypt not-sus.pdf -i
                decrypts not-sus.pdf in-place.
            pdfriend decrypt balance.pdf -o balance-decrypted.pdf
                decrypts balance.pdf and saves to balance-decrypted.pdf.
            pdfriend decrypt acct.pdf
                decrypts acct.pdf and saves to pdfriend_output.pdf.
    """),
    info.CommandInfo("metadata", "M", descr = """ [filename] [--get key?] [--set key_val_pairs?] [--pop keys?]
        manages PDF metadata. Using no extra flags, it will print the key-value pairs. You can use --get to print the value of a specific key and --set to set values for keys, or --pop to delete them.

        examples:
            pdfriend metadata some.pdf
                prints the metadata of some.pdf.
            pdfriend metadata thing.pdf --get /Author
                prints the name of the author of the PDF, if that field has been set.
            pdfriend metadata stolen.pdf --set /Author=me
                sets the author of stolen.pdf to "me". BEWARE: This will overwrite the PDF, unlike most of the other pdfriend commands.
            pdfriend metadata cnp.pdf --set  "/Title=Crime And Punishment"
                sets the title to that. Note that you need the quotes here, else your shell will interpret the words as different arguments.
            pdfriend metadata phys1.pdf --set "/Title=University Physics with Modern Physics,/Author=H. Young and R. Freedman"
                sets the author of phys1.pdf to "H. Young and R. Freedman" and its title to you-know-what.
            pdfriend metadata embarassing_fanfic.pdf --pop /Author
                removes (!) the PDF's author field.
            pdfriend metadata mystery.pdf --pop /Author,/Producer
                removes the PDF's author and producer fields.
    """),
    foreword = """pdfriend: a command line utility for easily modifying PDF files
    usage: pdfriend [command] [arguments?] [-d|--debug?] (note that options in [] are required and options in [?] are not). Use -d or --debug for more detailed error messages.
    the following commands are available:
    """,
    postword = """use pdfriend help [command] to get the instructions for particular commands"""
)

def run_pdfriend(args):
    try:
        cmd_parser = cmdparsers.CmdParser.FromArgs(
            program_info,
            args.commands,
            no_command_message = "No command specified! Use pdfriend help to get a list of the available commands"
        )

        short = cmd_parser.short()

        if short == "v" or args.version:
            print(commands.version())
        elif short == "h" or args.help:
            command_to_display = cmd_parser.next_str_or(None)
            print(program_info.help(command_to_display))
        elif short == "m":
            if len(cmd_parser.args) == 0:
                print("You need to specify at least one file or pattern to be merged")
                return

            commands.merge(cmd_parser.args, args.outfile, args.quality)
        elif short == "e":
            pdf = cmd_parser.next_pdf("filename")

            # I have to do this because args.import is a syntax error
            # for some reason. Must be messing with the import keyword?
            import_file = args.__getattribute__("import")
            import_args = None
            if import_file is not None:
                import_args = cmdparsers.to_shell_import(import_file)

            commands.edit(pdf, commands = import_args, open_pdf = Config.OpenPDFs)
        elif short == "t":
            pdf = cmd_parser.next_pdf("filename")

            # I have to do this because args.import is a syntax error
            # for some reason. Must be messing with the import keyword?
            import_file = args.__getattribute__("import")
            import_args = None
            if import_file is not None:
                import_args = cmdparsers.to_shell_import(import_file)

            commands.tinker(pdf, commands = import_args, open_pdf = Config.OpenPDFs)
        elif short == "i":
            pdf = cmd_parser.next_pdf("filename")

            if args.inplace:
                args.outfile = pdf.source

            commands.invert(pdf, args.outfile)
        elif short == "c":
            subcommand = cmd_parser.next_str("subcommand")

            commands.cache(subcommand)
        elif short == "w":
            pdf_0 = cmd_parser.next_pdf("filename_0")
            pdf_1 = cmd_parser.next_pdf("filename_1")

            commands.weave(pdf_0, pdf_1, args.outfile)
        elif short == "s":
            pdf = cmd_parser.next_pdf("filename")
            slice = cmd_parser.next_pdf_slice(pdf, name = "pages")

            commands.split(pdf, slice, args.outfile)
        elif short == "g":
            pdf = cmd_parser.next_pdf("filename")
            slice = cmd_parser.next_pdf_slice(pdf, name = "pages")

            if args.inplace:
                args.outfile = pdf.source

            commands.get(pdf, slice, args.outfile)
        elif short == "n":
            pdf = cmd_parser.next_pdf("filename")

            if args.inplace:
                args.outfile = pdf.source

            commands.encrypt(pdf, args.outfile)
        elif short == "d":
            infile = cmd_parser.next_file("filename")

            if args.inplace:
                args.outfile = infile

            commands.decrypt(infile, args.outfile)
        elif short == "meta":
            pdf = cmd_parser.next_pdf("filename")

            commands.metadata(pdf, args.get, args.set, args.pop)
        else:
            print(f"command \"{cmd_parser.name()}\" not recognized")
            print("use pdfriend help for a list of the available commands")
    except exceptions.ExpectedError as e:
        if Config.Debug:
            print(traceback.format_exc())
        else:
            print(e)
    except Exception as e:
        utils.print_unexpected_exception(e, Config.Debug)


def main():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("commands", type=str, nargs="*")

    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")

    parser.add_argument("-o", "--outfile", type=str, default="pdfriend_output")
    parser.add_argument("-i", "--inplace", action="store_true")
    parser.add_argument("-q", "--quality", type=int, default=100)
    parser.add_argument("-I", "--import", type=str, default=None)

    parser.add_argument("--get", type=str, default=None)
    parser.add_argument("--set", type=str, default=None)
    parser.add_argument("--pop", type=str, default=None)

    args = parser.parse_args()

    Platform.Init()
    Config.Debug = args.debug

    run_pdfriend(args)

