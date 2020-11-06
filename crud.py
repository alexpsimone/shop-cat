from model import db, User, Procedure, Page, Car, Part, Tool
from model import PartNum, ProcedureCar, ProcedurePart, ProcedureTool

def create_user(username, password, nickname, img):
    """Create and return a new user."""

    user = User(username = username,
                password = password,
                nickname = nickname,
                avatar_img_url = img
                )

    db.session.add(user)
    db.session.commit()

    return user


def create_page(size, page_url, page_type):
    """Create and return a new user."""

    page = Page(size = size,
                page_url = page_url,
                page_type = page_type
                )

    db.session.add(page)
    db.session.commit()

    return page


def create_procedure(title, description, label, img, user, page):
    """Create and return a new user."""

    procedure = Procedure(title = title,
                description = description,
                label = label,
                img = img,
                user = user,
                page = page
                )

    db.session.add(procedure)
    db.session.commit()

    return procedure