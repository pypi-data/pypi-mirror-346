import pdfriend.classes.wrappers as wrappers
import pypdf
import getpass

def decrypt(infile: str, outfile: str):
    pdf = pypdf.PdfReader(infile)

    if pdf.is_encrypted:
        password = getpass.getpass("password: ")

        pdf.decrypt(password)

    wrapper = wrappers.PDFWrapper(pages = pdf.pages)
    wrapper.write(outfile)

