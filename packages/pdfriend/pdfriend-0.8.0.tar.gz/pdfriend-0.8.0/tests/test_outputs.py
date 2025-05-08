from helpers.file_existence import check_one_output_command
from helpers.managers import FileManager

fm = FileManager.New()


def test_invert():
    path = "model.pdf"
    fm.new_pdf(path, range(10))

    assert check_one_output_command(
        commands = ["invert", path],
        input = path,
    )

    fm.delete_all()
