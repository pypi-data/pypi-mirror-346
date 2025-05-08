import getpass
import pathlib
import pdfriend.classes.wrappers as wrappers


def encrypt(pdf: wrappers.PDFWrapper, outfile: str):
    password = getpass.getpass("password: ")
    # if the input doesn't get overwritten, there's no need to
    # double check the password
    if pdf.source == outfile:
        confirmation = getpass.getpass("repeat the password: ")
        if password != confirmation:
            print("the passwords don't match!")
            return

    writer = pdf.to_writer()
    writer.encrypt(password)
    writer.write(pathlib.Path(outfile).with_suffix(".pdf"))
