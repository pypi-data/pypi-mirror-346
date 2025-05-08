import pdfriend.classes.wrappers as wrappers


def invert(pdf: wrappers.PDFWrapper, outfile: str):
    pdf.pages_invert().write(outfile)
