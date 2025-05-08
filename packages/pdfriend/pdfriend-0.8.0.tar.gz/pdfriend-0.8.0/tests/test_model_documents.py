from pdfriend.classes.platforms import Platform
from helpers.model_documents import ModelPDF


def test_model_documents():
    p0 = ModelPDF.New(range(10))
    p1 = ModelPDF.New(range(10))
    assert p0 == p1

    model_pdf_path = Platform.NewTemp("some_model_pdf.pdf")
    p1.save(model_pdf_path)
    p2 = ModelPDF.Read(model_pdf_path)

    assert p0 == p2
    assert p1 == p2

    p3 = ModelPDF.New(range(1,11))
    assert not p0 == p3

    p4 = ModelPDF.New([])
    assert p4.is_empty()

    model_pdf_path.unlink()
