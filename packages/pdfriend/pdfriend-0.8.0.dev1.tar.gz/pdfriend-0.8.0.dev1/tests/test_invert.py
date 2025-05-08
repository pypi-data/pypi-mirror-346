from pdfriend.main import run_pdfriend
from helpers.flags import make_args
from helpers.managers import FileManager
from helpers.model_documents import ModelPDF
from pathlib import Path


def test_invert():
    fm = FileManager.New()
    pages = list(range(10))
    path, path_inv = Path("model.pdf"), Path("model_inv.pdf")
    fm.new_pdf(path, pages)
    fm.register(path_inv)

    run_pdfriend(make_args(["invert", path], outfile = path_inv))

    pdf_inv = ModelPDF.Read(path_inv)

    assert pdf_inv == ModelPDF(pages[::-1])

    fm.delete_all()
