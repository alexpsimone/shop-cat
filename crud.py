from model import db, connect_to_db, User, Procedure, Car, Part, Tool, Step
from model import PartNum, ProcedureCar, ProcedurePart, ProcedureTool
import requests
import os
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
from server import app


def allowed_file(filename):
    """from Flask docs: confirm an uploaded img has correct extension"""

    allowed_extensions = {"png", "jpg", "jpeg"}

    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def get_step_ref_and_img(is_ref, reference, step_img):
    """Determine if a reference and/or img needs to be added to the Step.

    Check to see if reference or image checkboxes were selecteed.
    If they were, then look to the corresponding input fields for data.
    Add image and reference info to the Step objects as required.
    """
    if is_ref:
        if "youtube.com" in reference:
            ref_remove_https = reference.replace("https://", "")
            ref_remove_www = ref_remove_https.replace("www.youtube.com/watch?v=", "")
            ref_text = ref_remove_www[:11]
        else:
            ref_text = reference
        if step_img and allowed_file(step_img.filename):
            filename = secure_filename(step_img.filename)
            step_img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            step_img.close()
        else:
            filename = "toolbox.png"
    else:
        ref_text = "No Ref Provided"
        if step_img and allowed_file(step_img.filename):
            filename = secure_filename(step_img.filename)
            step_img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            step_img.close()
        else:
            filename = "toolbox.png"

    return [ref_text, filename]


def create_tool(req_name, other_name, tool_img):
    """Determine if a tool is new, and if so, then create one.

    Check if the user selected an existing tool.
    If they did, then keep it handy, and don't create a new Tool object.
    If they didn't, then double-check that the tool is actually new.
    If it isn't, then select the corresponding existing tool.
    Otherwise. create a new Tool object with the new info.
    """

    if req_name != "other":
        my_tool = Tool.query.filter_by(name=req_name).first()
    elif Tool.query.filter_by(name=other_name).first() != None:
        my_tool = Tool.query.filter_by(name=other_name).first()
    else:
        if tool_img and allowed_file(tool_img.filename):
            filename = secure_filename(tool_img.filename)
            tool_img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            tool_img.close()
        else:
            filename = "toolbox.png"
        my_tool = Tool(name=other_name, tool_img=filename)
        db.session.add(my_tool)

    return my_tool


def create_part(req_name, other_name, part_img, other_num, other_manuf, is_oem):
    """Determine if a part is new, and if so, then create one.

    Check if the user selected an existing part.
    If they did, then keep it handy, and don't create a new Part object.
    If they didn't, then double-check that the part is actually new.
    If it isn't, then select the corresponding existing part.
    Otherwise. create a new Part object with the new info.
        This will also require a new PartNumber object."""

    if req_name != "other":
        my_part = Part.query.filter_by(name=req_name).first()
    elif Part.query.filter_by(name=other_name).first() != None:
        my_part = Part.query.filter_by(name=other_name).first()
    else:
        if part_img and allowed_file(part_img.filename):
            filename = secure_filename(part_img.filename)
            part_img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            part_img.close()
        else:
            filename = "toolbox.png"
        my_part = Part(name=other_name, part_img=filename)
        # *#*#*#*#*#*#*#*#*#*#*#*#*#*
        db.session.add(my_part)
        part_num = PartNum(
            manuf=other_manuf, part_num=other_num, is_oem_part=is_oem, part=my_part
        )
        # *#*#*#*#*#*#*#*#*#*#*#*#*#*
        db.session.add(part_num)

    return my_part

#################################################
#### TODO: Break down into smaller functions. ###
#################################################
def update_procedure(proc_id, title, label, cars, tool_data, part_data, step_data):
    """Update a Procedure with given information."""

    proc = Procedure.query.filter_by(proc_id=proc_id).first()

    # Update procedure.title.
    proc.title = title

    # Update procedure.label.
    proc.label = label

    # Update which vehicles are associated with the procedure.
    car_ids = set()

    for item in cars:
        car_info = item.split("-") # Returns [model_year, make, model] for each car.
        car = Car.query.filter(
            Car.model_year == car_info[0],
            Car.make == car_info[1],
            Car.model == car_info[2],
        ).first()
        if car:
            if not ProcedureCar.query.filter_by(car_id=car.car_id):
                proc_car = ProcedureCar(proc=proc, car=car)
                db.session.add(proc_car)
                # *#*#*#*#*#*#*#*#*#*#*#*#*#*
                db.session.commit()

        else:
            car = Car(model=car_info[2], make=car_info[1], model_year=car_info[0])
            db.session.add(car)
            proc_car = ProcedureCar(proc=proc, car=car)
            db.session.add(proc_car)
            # *#*#*#*#*#*#*#*#*#*#*#*#*#*
            db.session.commit()

        car_ids.add(car.car_id)

    # Check all ProcedureCar objects associated with this procedure.
    # If a ProcedureCar object includes a car ID that isn't in car_ids,
    # delete that ProcedureCar.
    # If that car ID is NOT present in any other ProcedureCar objects, then
    # delete that Car.
    proc_cars_by_proc = ProcedureCar.query.filter_by(proc_id=proc_id).all()

    for proc_car_by_proc in proc_cars_by_proc:
        if proc_car_by_proc.car_id not in car_ids:
            db.session.delete(proc_car_by_proc)
            proc_cars_by_car = ProcedureCar.query.filter_by(
                car_id=proc_car_by_proc.car_id
            ).all()
            if proc_cars_by_car == []:
                db.session.delete(
                    Car.query.filter_by(car_id=proc_car_by_proc.car_id).first()
                )

    # Go through tool_data and make sure all tool info is updated.
    # Add any new tools and procedure-tool objects to the database.
    tool_ids = set()
    for item in tool_data:
        if tool_data[item]["id"] != "NEW":
            tool = Tool.query.filter_by(tool_id=int(tool_data[item]["id"])).first()
            if tool_data[item]["name"] != tool.name:
                tool.name = tool_data[item]["name"]
            if tool_data[item]["img"] != tool.tool_img:
                tool.tool_img = tool_data[item]["img"]
            tool_ids.add(int(tool_data[item]["id"]))
        else:
            if tool_data[item]["name"] == "other":
                if Tool.query.filter_by(name=tool_data[item]["other"]).first() != None:
                    tool = Tool.query.filter_by(name=tool_data[item]["other"]).first()
                    tool_ids.add(tool.tool_id)
                else:
                    tool = Tool(
                        name=tool_data[item]["other"], tool_img=tool_data[item]["img"]
                    )
                    db.session.add(tool)
                    db.session.commit()
                    tool_ids.add(tool.tool_id)
            else:
                tool = Tool.query.filter_by(name=tool_data[item]["name"]).first()
                tool_ids.add(tool.tool_id)
            if (
                ProcedureTool.query.filter(
                    ProcedureTool.tool_id == tool.tool_id,
                    ProcedureTool.proc_id == proc.proc_id,
                ).first()
                == None
            ):
                proc_tool = ProcedureTool(proc=proc, tool=tool)
                db.session.add(proc_tool)
                db.session.commit()
    # Check all ProcedureTool objects associated with this procedure.
    # If a ProcedureTool object includes a tool ID that isn't in tool_data,
    # delete that ProcedureTool.
    proc_tools = ProcedureTool.query.filter_by(proc_id=proc.proc_id).all()

    for proc_tool in proc_tools:
        if proc_tool.tool_id not in tool_ids:
            db.session.delete(proc_tool)

    # Go through part_data and make sure all part info is updated.
    # Add any new parts, part numbers, and procedure-part objects to the db.
    part_ids = set()
    for item in part_data:
        if part_data[item]["id"] != "NEW":
            part = Part.query.filter_by(part_id=part_data[item]["id"]).first()
            if part_data[item]["name"] != part.name:
                part.name = part_data[item]["name"]
            if part_data[item]["img"] != part.part_img:
                part.part_img = part_data[item]["img"]
            part_ids.add(int(part_data[item]["id"]))
        else:
            if part_data[item]["name"] == "other":
                if Part.query.filter_by(name=part_data[item]["other"]).first() != None:
                    part = Part.query.filter_by(name=part_data[item]["other"]).first()
                    part_ids.add(part.part_id)
                else:
                    part = Part(
                        name=part_data[item]["other"], part_img=part_data[item]["img"]
                    )
                    db.session.add(part)
                    db.session.commit()
                    part_num = PartNum(
                        manuf=part_data[item]["manuf"],
                        part_num=part_data[item]["pn"],
                        is_oem_part=part_data[item]["oem"],
                        part=part,
                    )
                    db.session.add(part_num)
                    part_ids.add(part.part_id)
            else:
                part = Part.query.filter_by(name=part_data[item]["name"]).first()
                part_ids.add(part.part_id)
            if (
                ProcedurePart.query.filter(
                    ProcedurePart.part_id == part.part_id,
                    ProcedurePart.proc_id == proc.proc_id,
                ).first()
                == None
            ):
                proc_part = ProcedurePart(proc=proc, part=part)
                db.session.add(proc_part)
                db.session.commit()

    # Check all ProcedurePart objects associated with this procedure.
    # If a ProcedurePart object includes a part ID that isn't in part_data,
    # delete that ProcedurePart.
    proc_parts = ProcedurePart.query.filter_by(proc_id=proc.proc_id).all()

    for proc_part in proc_parts:
        if proc_part.part_id not in part_ids:
            db.session.delete(proc_part)

    # Go through step_data and make sure all step info is updated.
    # Add any new steps to the database.
    # step_data: (step_id, step_order, step_text, step_ref, step_img)

    step_ids = set()
    for item in step_data:
        if step_data[item]["id"] != "NEW":
            step = Step.query.filter_by(step_id=step_data[item]["id"]).first()
            if step_data[item]["order"] != step.order_num:
                step.order_num = step_data[item]["order"]
            if step_data[item]["text"] != step.step_text:
                step.text = step_data[item]["text"]
            if step_data[item]["ref"] != step.reference:
                if step_data[item]["ref"] == "" or step_data[item]["ref"] == None:
                    step.reference = "No Ref Provided"
                else:
                    step.reference = step_data[item]["ref"]
            if step_data[item]["img"] != step.step_img:
                step.step_img = step_data[item]["img"]
            step_ids.add(int(step_data[item]["id"]))
        else:
            if step_data[item]["ref"] == "" or step_data[item]["ref"] == None:
                step_data[item]["ref"] = "No Ref Provided"

            step = Step(
                order_num=step_data[item]["order"],
                step_text=step_data[item]["text"],
                proc_id=proc.proc_id,
                reference=step_data[item]["ref"],
                step_img=step_data[item]["img"],
            )

            db.session.add(step)
            db.session.commit()
            step_ids.add(step.step_id)

    # Check all Step objects associated with this procedure.
    # If a Step object includes a step ID that isn't in part_data,
    # delete that Step.
    steps = Step.query.filter_by(proc_id=proc.proc_id).all()

    for step in steps:
        if step.step_id not in step_ids:
            db.session.delete(step)

    db.session.commit()

    return proc


def get_all_rockauto_makes():
    """Scrape all vehicle makes from RockAuto's website."""

    url = "http://www.rockauto.com"
    req = requests.get(url)
    src = req.content
    soup = BeautifulSoup(src, "lxml")

    divs_normal = soup.findAll("a", {"class": "navlabellink nvoffset nnormal"})
    divs_important = soup.findAll("a", {"class": "navlabellink nvoffset nimportant"})
    car_makes_normal = [div_normal.string for div_normal in divs_normal]
    car_makes_important = [div_important.string for div_important in divs_important]

    return sorted(car_makes_normal + car_makes_important)


def get_all_rockauto_model_years(make):
    """Scrape all model years for a given make from RockAuto's website."""

    make_split = make.split(" ")
    make_join = "+".join(make_split)

    url = f"http://www.rockauto.com/en/catalog/{make_join}"
    req = requests.get(url)
    src = req.content
    soup = BeautifulSoup(src, "lxml")

    divs_normal = soup.findAll("a", {"class": "navlabellink nvoffset nnormal"})
    model_years = [div_normal.string for div_normal in divs_normal][1:]

    return model_years


def get_all_rockauto_models(make, model_year):
    """Scrape all models for a given model_year and make from RockAuto's website."""

    make_split = make.split(" ")
    make_join = "+".join(make_split)

    url = f"http://www.rockauto.com/en/catalog/{make_join},{model_year}"
    req = requests.get(url)
    src = req.content
    soup = BeautifulSoup(src, "lxml")

    divs_normal = soup.findAll("a", {"class": "navlabellink nvoffset nnormal"})
    models = [div_normal.string for div_normal in divs_normal][2:]

    return sorted(models)
