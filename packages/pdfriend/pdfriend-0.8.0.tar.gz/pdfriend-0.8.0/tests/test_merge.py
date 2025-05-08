from pdfriend.main import run_pdfriend
from helpers.flags import make_args
from helpers.managers import FileManager
from helpers.model_documents import ModelPDF
from pathlib import Path


def test_merge():
    fm = FileManager.New()
    input_pages = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
    ]
    output_pages = []
    input_paths = []

    for idx, pages in enumerate(input_pages):
        output_pages.extend(pages)
        input_path = Path(f"model_{idx}.pdf")
        input_paths.append(str(input_path))
        fm.new_pdf(input_path, pages)

    output_path = Path("model.pdf")
    fm.register(output_path)

    run_pdfriend(make_args(
        ["merge", *input_paths],
        outfile = output_path
    ))

    output_pdf = fm.read_pdf(output_path)
    assert output_pdf == ModelPDF(output_pages)

    fm.delete_all()


if __name__ == "__main__":
    test_merge()
