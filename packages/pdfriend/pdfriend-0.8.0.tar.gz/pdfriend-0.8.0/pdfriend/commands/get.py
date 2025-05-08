import pdfriend.classes.wrappers as wrappers
import pathlib


def get(pdf: wrappers.PDFWrapper, slice: list[int], outfile: str | pathlib.Path):
    pdf.pages_subset(slice).write(outfile)
