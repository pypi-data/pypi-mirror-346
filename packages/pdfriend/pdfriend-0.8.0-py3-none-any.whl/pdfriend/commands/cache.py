from pdfriend.classes.platforms import Platform
import shutil

def cache(subcommand: str):
    if subcommand == "clear":
        if Platform.BackupDir.exists():
            shutil.rmtree(Platform.BackupDir.as_posix())

        Platform.BackupDir.mkdir()
