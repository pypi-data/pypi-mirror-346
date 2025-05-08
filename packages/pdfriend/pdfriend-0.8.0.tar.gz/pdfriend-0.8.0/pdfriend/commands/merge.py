import glob
import os
import pdfriend.classes.wrappers as wrappers
from pdfriend.classes.platforms import Platform

IMAGE_FORMATS = {
    ".png", ".jpg", ".jpeg", ".jpe", "jfif",
    ".j2c", ".j2k", ".jp2", ".jpc", ".jpf", ".jpx",
    ".webp", ".bmp", ".eps", ".ps",
    ".kra"  # we can extract images from krita files
}


# expands all globs in list: can contain both patterns and single filenames,
# doesn't matter, it will eat them all
def globs_to_filenames(globs: list[str]) -> list[str]:
    result = []
    for g in globs:
        result.extend(glob.glob(g))

    return result


def images_to_pdf(filenames: list[str], outfile: str, quality: int):
    images = wrappers.ImageWrapper.FromFiles(filenames)
    images.equalize_widths()
    images.write(outfile, quality)


# unfortunately, the easiest way to do this is to write the pdf into a temporary
# file and read it again
def images_to_pdf_wrapper(filenames: list[str], quality: int) -> wrappers.PDFWrapper:
    tempfile: str = Platform.NewTemp("temp.pdf").as_posix()

    images_to_pdf(filenames, tempfile, quality)
    pdf = wrappers.PDFWrapper.Read(tempfile)
    os.remove(tempfile)

    return pdf


def merge(globs: list[str], outfile: str, quality: int):
    filenames = globs_to_filenames(globs)

    final_pdf = wrappers.PDFWrapper()
    buffer = []  # for images to be merged into pdf

    for filename in filenames:
        _, extension = os.path.splitext(filename)

        if extension in IMAGE_FORMATS:
            buffer.append(filename)
        else:  # when the block of images ends, merge them into a pdf
            if len(buffer) > 0:
                pdf = images_to_pdf_wrapper(buffer, quality)
                buffer = []

                final_pdf.pages_merge(pdf)

            if extension == ".pdf":
                pdf = wrappers.PDFWrapper.Read(filename)
                final_pdf.pages_merge(pdf)

            # note that if it's neither image nor a pdf, it is ignored

    if len(buffer) > 0:  # in case the filename list ends with images
        # this is for efficiency, in case all files are images: otherwise
        # backend.images_to_df_wrapper would write the pdf, read it, delete it
        # and then final_pdf.write would write it again. Instead we just write
        if final_pdf.pages_len() == 0:
            images_to_pdf(buffer, outfile, quality)
            return

        pdf = images_to_pdf_wrapper(buffer, quality)
        final_pdf.pages_merge(pdf)

    final_pdf.write(outfile)
