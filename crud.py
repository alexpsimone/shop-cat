from model import db, connect_to_db, User, Procedure, Car, Part, Tool
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


# def create_page(size, page_url, page_type):
#     """Create and return a page."""

#     page = Page(size = size,
#                 page_url = page_url,
#                 page_type = page_type
#                 )

#     db.session.add(page)
#     db.session.commit()

#     return page


def create_procedure(title, description, label, img, user):
    """Create and return a procedure."""

    procedure = Procedure(title = title,
                description = description,
                label = label,
                img = img,
                user = user,
                )

    db.session.add(procedure)
    db.session.commit()

    return procedure


def create_car(model, make, model_year):
    """Create and return a car."""

    car = Car(model = model, 
                make = make, 
                model_year = model_year
                )

    db.session.add(car)
    db.session.commit()

    return car


def create_tool(name, description, tool_img):
    """Create and return a tool."""

    tool = Tool(name = name,
                description = description,
                tool_img = tool_img
                )

    db.session.add(tool)
    db.session.commit()

    return tool


def create_procedure_tool(proc, tool):
    """Create and return a ProcedureTool object."""

    proc_tool = ProcedureTool(proc = proc, tool = tool)

    db.session.add(proc_tool)
    db.session.commit()

    return proc_tool


def create_part(name, part_img):
    """Create and return a part."""

    part = Part(name = name, part_img = part_img)

    db.session.add(part)
    db.session.commit()

    return part


def create_part_num(manuf, part_num, is_oem_part, part):
    """Create and return a part number."""

    part_num = PartNum(manuf = manuf, 
                        part_num = part_num,
                        is_oem_part = is_oem_part,
                        part = part)

    db.session.add(part_num)
    db.session.commit()

    return part_num


def create_procedure_part(proc, part):
    """Create and return a ProcedureTool object."""

    proc_part = ProcedurePart(proc = proc, part = part)

    db.session.add(proc_part)
    db.session.commit()

    return proc_part


def create_procedure_car(proc, car):
    """Create and return a ProcedureCar object."""

    proc_car = ProcedureCar(proc = proc, car = car)

    db.session.add(proc_car)
    db.session.commit()

    return proc_car


def create_procedure_car(proc, car):
    """Create and return a ProcedureCar object."""

    proc_car = ProcedureCar(proc = proc, car = car)

    db.session.add(proc_car)
    db.session.commit()

    return proc_car


def get_cars():
    """Return all cars."""

    return Car.query.all()


def get_procedures():
    """Return all procedures."""

    return Procedure.query.all()


def get_tools():
    """Return all tools."""

    return Tool.query.all()


def get_parts():
    """Return all parts."""

    return Part.query.all()


def get_procedure_by_id(proc_id):
    """Return a procedure with a given proc_id."""

    return Procedure.query.get(proc_id)


def get_proc_car_by_proc_id(proc_id):
    """Return all proc_car objects associated with a given proc_id."""
    
    return ProcedureCar.query.filter_by(proc_id = proc_id).all()


def get_parts_by_proc_id(proc_id):
    """Return all parts associated with a given proc_id."""

    return ProcedurePart.query.filter_by(proc_id = proc_id).all()


def get_tools_by_proc_id(proc_id):
    """Return all tools associated with a given proc_id."""
    
    return ProcedureTool.query.filter_by(proc_id = proc_id).all()


def get_car_by_details(model_year, make, model):
    """Return a car with the specified info, if it exists."""

    return Car.query.filter_by(model_year = model_year, make = make, model = model).first()


def get_user_by_id(user_id):
    """Get a user with a given ID."""

    return User.query.filter_by(user_id = user_id).first()