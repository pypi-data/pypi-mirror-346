import pypdf


def rotate(page: pypdf.PageObject, angle: float) -> pypdf.PageObject:
    int_angle = int(angle)
    if int_angle % 90 == 0 and (angle - int_angle) < 0.0001:
        page.rotate(int_angle)
    else:
        rotation = pypdf.Transformation().rotate(angle)
        page.add_transformation(rotation)

    return page
