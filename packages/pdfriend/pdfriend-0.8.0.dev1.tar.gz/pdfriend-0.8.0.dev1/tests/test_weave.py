from pdfriend.main import run_pdfriend
from helpers.flags import make_args
from helpers.managers import FileManager
from helpers.model_documents import ModelPDF
from pathlib import Path


def test_weave():
    fm = FileManager.New()

    pages_0 = list(range(10))
    pages_1 = [-page for page in pages_0]
    path_0, path_1, path_out = Path("model_0.pdf"), Path("model_1.pdf"), Path("model_out.pdf")
    fm.new_pdf(path_0, pages_0)
    fm.new_pdf(path_1, pages_1)
    fm.register(path_out)

    run_pdfriend(make_args(
        ["weave", path_0, path_1],
        outfile = path_out
    ))

    pdf_out = ModelPDF.Read(path_out)

    correct_model = []
    for page_0, page_1 in zip(pages_0, pages_1):
        correct_model.extend([page_0, page_1])

    assert pdf_out == ModelPDF(correct_model)

    fm.delete_all()
