from model import db, connect_to_db, User, Procedure, Car, Part, Tool, Step
from model import PartNum, ProcedureCar, ProcedurePart, ProcedureTool
import requests
from bs4 import BeautifulSoup


def allowed_file(filename):
    """from Flask docs: confirm an uploaded img has correct extension"""
    
    allowed_extensions = {'png', 'jpg', 'jpeg'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def check_toolbox(tool_name):
    """Check if a tool is in the existing toolbox."""
    
    return Tool.query.filter_by(name = tool_name).first()


def check_parts_bin(part_name):
    """Check if a part is in the existing parts bin."""

    return Part.query.filter_by(name = part_name).first()


def create_car(model, make, model_year):
    """Create and return a car."""

    car = Car(model = model, 
                make = make, 
                model_year = model_year
                )

    db.session.add(car)
    db.session.commit()

    return car


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


def create_procedure(title, label, user):
    """Create and return a procedure."""

    procedure = Procedure(title = title, label = label, user = user)

    db.session.add(procedure)
    db.session.commit()

    return procedure


def create_procedure_car(proc, car):
    """Create and return a ProcedureCar object."""

    proc_car = ProcedureCar(proc = proc, car = car)

    db.session.add(proc_car)
    db.session.commit()

    return proc_car


def create_procedure_part(proc, part):
    """Create and return a ProcedureTool object."""

    proc_part = ProcedurePart(proc = proc, part = part)

    db.session.add(proc_part)
    db.session.commit()

    return proc_part


def create_procedure_tool(proc, tool):
    """Create and return a ProcedureTool object."""

    proc_tool = ProcedureTool(proc = proc, tool = tool)

    db.session.add(proc_tool)
    db.session.commit()

    return proc_tool


def create_step(order_num, step_text, proc, reference, step_img):

    """Create and return a Step object."""

    step = Step(order_num = order_num, 
                step_text = step_text, 
                proc = proc,
                reference = reference,
                step_img = step_img)

    db.session.add(step)
    db.session.commit()

    return step


def create_tool(name, tool_img='toolbox.png'):
    """Create and return a tool."""

    tool = Tool(name = name,
                tool_img = tool_img
                )

    db.session.add(tool)
    db.session.commit()

    return tool


def create_user(username, password, nickname="nothingyet", img="emptypath"):
    """Create and return a new user."""

    user = User(username = username,
                password = password,
                nickname = nickname,
                avatar_img_url = img
                )

    db.session.add(user)
    db.session.commit()

    return user


def get_car_by_details(model_year, make, model):
    """Return a car with the specified info, if it exists."""

    return Car.query.filter_by(model_year = model_year, 
                                make = make, model = model).first()


def get_cars():
    """Return all cars."""

    return Car.query.all()


def get_cars_by_make(make):
    """Return all Car objects with a given model year."""

    return Car.query.filter_by(make = make).all()


def get_cars_by_make_and_model_year(make, model_year):
    """Return all Car objects with a given make and model year."""

    return Car.query.filter(Car.make == make, Car.model_year == model_year).all()


def get_parts():
    """Return all parts."""

    return Part.query.all()


def get_parts_by_proc_id(proc_id):
    """Return all parts associated with a given proc_id."""

    return ProcedurePart.query.filter_by(proc_id = proc_id).all()


def get_procedure_by_id(proc_id):
    """Return a procedure with a given proc_id."""

    return Procedure.query.get(proc_id)


def get_procedures():
    """Return all procedures."""

    return Procedure.query.all()


def get_proc_car_by_proc_id(proc_id):
    """Return all proc_car objects associated with a given proc_id."""
    
    return ProcedureCar.query.filter_by(proc_id = proc_id).all()


def get_proc_car_by_car_info(make, model_year, model):
    """Return all proc_car objects associated with a given car."""

    car = Car.query.filter(Car.make == make, 
                            Car.model_year == model_year, 
                            Car.model == model).first()
      
    return ProcedureCar.query.filter_by(car_id = car.car_id).all()


def get_steps_by_proc_id(proc_id):
    """Return all Step objects associated with a given proc_id."""
    
    return Step.query.filter_by(proc_id = proc_id).all()


def get_tools():
    """Return all tools."""

    return Tool.query.all()


def get_tool_by_id(tool_id):
    """Return a tool with a given id."""

    return Tool.query.filter_by(tool_id = tool_id).first()


def get_tools_by_proc_id(proc_id):
    """Return all tools associated with a given proc_id."""
    
    return ProcedureTool.query.filter_by(proc_id = proc_id).all()


def get_user_by_id(user_id):
    """Get a user with a given ID."""

    return User.query.filter_by(user_id = user_id).first()


def get_user_by_username(username):
    """Get a user with a given username."""

    return User.query.filter_by(username = username).first()


def num_cars_by_proc(proc_id):
    """Return the number of cars associated with a given procedure."""

    return ProcedureCar.query.filter_by(proc_id = proc_id).count()


def num_parts_by_proc(proc_id):
    """Return the number of tools required for a given procedure."""

    return ProcedurePart.query.filter_by(proc_id = proc_id).count()


def num_steps_by_proc(proc_id):
    """Return the number of tools required for a given procedure."""

    return Step.query.filter_by(proc_id = proc_id).count()


def num_tools_by_proc(proc_id):
    """Return the number of tools required for a given procedure."""

    return ProcedureTool.query.filter_by(proc_id = proc_id).count()


def update_procedure(proc_id, title, remove_label, label, tool_data):
    """Update a Procedure with given information."""

    proc = Procedure.query.filter_by(proc_id = proc_id).first()

    # Update procedure.title.
    proc.title = title

    # Update procedure.label.
    if remove_label:
        proc.label = None
    elif label == '':
        proc.label = None
    else: 
        proc.label = label

    #############################################################
    ############ TODO: refactor w/o list indexing!! #############
    #############################################################
    # Go through tool_data and make sure all tool info is updated.
    # Add any new tools to the database.
    # tool_data: (tool_id, tool_name, tool_img, tool_other_name)
    tool_ids = set()
    for item in tool_data:
        if item[0] != "NEW":
            tool = Tool.query.filter_by(tool_id = item[0]).first()
            if item[1] != tool.name:
                tool.name = item[1]
            if item[2] != tool.tool_img:
                tool.tool_img = item[2]
            tool_ids.add(int(item[0]))
        else:
            if item[1] == 'other':
                if check_toolbox(item[3]) != None:
                    tool = Tool.query.filter_by(name = item[3]).first()
                    tool_ids.add(tool.tool_id)
                else:
                    tool = create_tool(item[3], item[2])
                    tool_ids.add(tool.tool_id)
            else:
                tool = Tool.query.filter_by(name = item[1]).first()
                tool_ids.add(tool.tool_id)
            create_procedure_tool(proc, tool)
    # Check all ProcedureTool items associated with this procedure.
    # If a ProcedureTool object includes a tool ID that isn't in tool_data,
    # delete that ProcedureTool.
    proc_tools = ProcedureTool.query.filter_by(proc_id = proc.proc_id).all()

    for proc_tool in proc_tools:
        if proc_tool.tool_id not in tool_ids:
            db.session.delete(proc_tool)
    
    #############################################################
    ############ TODO: refactor w/o list indexing!! #############
    #############################################################
    # Go through part_data and make sure all part info is updated.
    # Add any new parts to the database.
    
    db.session.commit()

    return proc


def get_all_rockauto_makes():
    """Scrape all vehicle makes from RockAuto's website."""

    url = 'http://www.rockauto.com'
    req = requests.get(url)
    src = req.content
    soup = BeautifulSoup(src, 'lxml')

    divs_normal = soup.findAll('a', {'class': 'navlabellink nvoffset nnormal'})
    divs_important = soup.findAll('a', {'class': 'navlabellink nvoffset nimportant'})
    car_makes_normal = [div_normal.string for div_normal in divs_normal]
    car_makes_important = [div_important.string for div_important in divs_important]

    return sorted(car_makes_normal + car_makes_important)