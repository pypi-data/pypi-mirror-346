from importlib.metadata import metadata

def version():
    return metadata("pdfriend")["Version"]
