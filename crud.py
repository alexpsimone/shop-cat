from model import db, User, Procedure, Page, Car, Part, Tool, PartNum, 
                    ProcedureCar, ProcedurePart, ProcedureTool

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