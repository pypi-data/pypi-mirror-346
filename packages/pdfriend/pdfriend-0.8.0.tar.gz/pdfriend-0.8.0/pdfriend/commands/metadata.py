import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.exceptions as exceptions


def metadata(
    pdf: wrappers.PDFWrapper,
    get: str | None = None,
    set_str: str | None = None,
    pop: str | None = None
):
    if get is not None:
        try:
            print(pdf.metadata[get])
        except KeyError:
            raise exceptions.ExpectedError(
                f"key \"{get}\" not found in the metadata.\navailable keys: {', '.join(list(pdf.metadata))}"
            )
    elif set_str is not None:
        for set_pair in set_str.split(","):
            set_pair_split = set_pair.split("=")
            if len(set_pair_split) < 2:
                raise exceptions.ExpectedError(f"no value provided for key {set_pair}")

            try:
                key, val = set_pair_split[0], set_pair_split[1]
                pdf.metadata[key] = val
                pdf.write()
            except Exception:
                raise exceptions.ExpectedError(f"metadata key \"{key}\" is invalid")
    elif pop is not None:
        keys_to_pop = pop.split(",")
        for key in keys_to_pop:
            del pdf.metadata[key]

        pdf.write()
    else:
        print("\n".join([f"{key}: {val}" for key, val in pdf.metadata.items()]))
