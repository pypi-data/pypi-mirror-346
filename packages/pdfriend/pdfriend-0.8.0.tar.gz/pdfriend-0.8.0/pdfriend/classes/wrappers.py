import pypdf
import shutil
import datetime
from PIL import Image
from typing import Self
from pathlib import Path
from zipfile import ZipFile

from .platforms import Platform
from .exceptions import ExpectedError
from ..ops.pages import PageContainer


class PDFWrapper(PageContainer):
    def __init__(
        self,
        source: Path = None,
        pages: list[pypdf.PageObject] = None,
        metadata: pypdf.DocumentInformation = None,
        reader: pypdf.PdfReader = None,
    ):
        self.source = source
        self.pages = pages or []
        self.metadata = metadata
        self.reader = reader
        if metadata is not None:
            self.metadata = dict(metadata)

    def get_pages(self) -> list[pypdf.PageObject]:
        return self.pages

    def set_pages(self, pages: list[pypdf.PageObject]) -> Self:
        self.pages = pages

    @classmethod
    def Read(cls, filename: str):
        pdf = pypdf.PdfReader(filename)

        return PDFWrapper(
            source = Path(filename),
            pages = list(pdf.pages),
            metadata = pdf.metadata,
            reader = pdf,
        )

    def reread(self, source: Path, keep_metadata: bool = True):
        new_pdf = PDFWrapper.Read(source)
        self.pages = new_pdf.pages
        if not keep_metadata:
            self.metadata = new_pdf.metadata

        return self

    def raise_if_out_of_range(self, page_num: int):
        if page_num >= 1 and page_num <= self.len():
            return
        raise ExpectedError(
            f"page {page_num} doesn't exist in the PDF (total pages: {self.len()})"
        )

    def to_writer(self):
        writer = pypdf.PdfWriter()
        if self.reader is not None and False:  # FIXME
            writer.clone_document_from_reader(self.reader)
        else:
            for page in self.pages:
                writer.add_page(page)

        return writer

    def write(self, filename: str = None, keep_metadata = True):
        if filename is None:
            filename = self.source

        writer = self.to_writer()
        if keep_metadata and self.metadata is not None:
            writer.add_metadata(self.metadata)

        writer.write(
            Path(filename).with_suffix(".pdf")
        )

    def backup(self, name: str | Path = None, copy: bool = True) -> Path:
        if name is None:
            name = self.source

        if not isinstance(name, Path):
            name = Path(name)

        now: str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        backup_file: Path = Platform.NewBackup(
            f"{name.stem}_{now}.pdf"
        )

        # prefer to just copy the file from the source if possible
        if copy and self.source.is_file():
            shutil.copyfile(self.source, backup_file)
        else:
            self.write(backup_file)

        return backup_file


def open_image(file: str|Path) -> Image:
    path = Path(file)
    if path.suffix == ".kra":
        with ZipFile(path, "r") as krita_file:
            return Image.open(krita_file.open("mergedimage.png", "r"))
    else:
        return Image.open(file)


def convert_to_rgb(img_rgba: Image.Image):
    try:
        img_rgba.load()
        _, _, _, alpha = img_rgba.split()

        img_rgb = Image.new("RGB", img_rgba.size, (255, 255, 255))
        img_rgb.paste(img_rgba, mask=alpha)

        return img_rgb
    except (IndexError, ValueError):
        return img_rgba


class ImageWrapper:
    def __init__(self, images: list[Image.Image]):
        self.images = [convert_to_rgb(image) for image in images]

    @classmethod
    def FromFiles(cls, filenames: list[str]) -> Self:
        return ImageWrapper([open_image(filename) for filename in filenames])

    def equalize_widths(self):
        max_width = max([image.size[0] for image in self.images])

        for i, image in enumerate(self.images):
            width, height = image.size

            scale = max_width / width

            self.images[i] = image.resize((max_width, int(height * scale)))

    def write(self, outfile: str, quality: int | float):
        self.images[0].save(
            outfile,
            "PDF",
            optimize=True,
            quality=int(quality),
            save_all=True,
            append_images=self.images[1:],
        )
