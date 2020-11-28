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
            ref_remove_https = reference.replace('https://', '')
            ref_remove_www = ref_remove_https.replace('www.youtube.com/watch?v=', '')
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
        my_tool = Tool(name = other_name, tool_img = filename)
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
        my_part = Part(name = other_name, part_img = filename)
        #*#*#*#*#*#*#*#*#*#*#*#*#*#*
        db.session.add(my_part)
        part_num = PartNum(manuf=other_manuf, part_num=other_num, is_oem_part=is_oem, part=my_part)
        #*#*#*#*#*#*#*#*#*#*#*#*#*#*
        db.session.add(part_num)
    
    return my_part
    


def update_procedure(
    proc_id, title, remove_label, label, cars, tool_data, part_data, step_data
):
    """Update a Procedure with given information."""

    proc = Procedure.query.filter_by(proc_id=proc_id).first()

    # Update procedure.title.
    proc.title = title

    # Update procedure.label.
    if remove_label:
        proc.label = None
    elif label == "":
        proc.label = None
    else:
        proc.label = label

    #############################################################
    ############ TODO: refactor w/o list indexing!! #############
    #############################################################
    # Update which vehicles are associated with the procedure.
    car_ids = set()

    for item in cars:
        car_info = item.split("-")
        car = Car.query.filter(
            Car.model_year == car_info[0],
            Car.make == car_info[1],
            Car.model == car_info[2],
        ).first()
        if car:
            if not ProcedureCar.query.filter_by(car_id=car.car_id):
                    proc_car = ProcedureCar(proc = proc, car = car)
                    #*#*#*#*#*#*#*#*#*#*#*#*#*#*
                    db.session.add(proc_car)
                    ###THIS COMMIT SEEMS TO MATTER!!!!!############
                    db.session.commit()

        else:
            car = Car(model=car_info[2], make=car_info[1], model_year=car_info[0])
            db.session.add(car)
            proc_car = ProcedureCar(proc = proc, car = car)
            #*#*#*#*#*#*#*#*#*#*#*#*#*#*
            db.session.add(proc_car)
            ###THIS COMMIT SEEMS TO MATTER!!!!!############
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

    #############################################################
    ############ TODO: refactor w/o list indexing!! #############
    #############################################################
    # Go through tool_data and make sure all tool info is updated.
    # Add any new tools to the database.
    # tool_data: (tool_id, tool_name, tool_img, tool_other_name)
    tool_ids = set()
    for item in tool_data:
        if item[0] != "NEW":
            tool = Tool.query.filter_by(tool_id=item[0]).first()
            if item[1] != tool.name:
                tool.name = item[1]
            if item[2] != tool.tool_img:
                tool.tool_img = item[2]
            tool_ids.add(int(item[0]))
        else:
            if item[1] == "other":
                if Tool.query.filter_by(name=item[3]).first() != None:
                    tool = Tool.query.filter_by(name=item[3]).first()
                    tool_ids.add(tool.tool_id)
                else:
                    tool = create_tool(item[3], item[2])
                    tool_ids.add(tool.tool_id)
            else:
                tool = Tool.query.filter_by(name=item[1]).first()
                tool_ids.add(tool.tool_id)
            if (
                ProcedureTool.query.filter(
                    ProcedureTool.tool_id == tool.tool_id,
                    ProcedureTool.proc_id == proc.proc_id,
                ).first()
                == None
            ):
                create_procedure_tool(proc, tool)
    # Check all ProcedureTool objects associated with this procedure.
    # If a ProcedureTool object includes a tool ID that isn't in tool_data,
    # delete that ProcedureTool.
    proc_tools = ProcedureTool.query.filter_by(proc_id=proc.proc_id).all()

    for proc_tool in proc_tools:
        if proc_tool.tool_id not in tool_ids:
            db.session.delete(proc_tool)

    #############################################################
    ############ TODO: refactor w/o list indexing!! #############
    #############################################################
    # Go through part_data and make sure all part info is updated.
    # Add any new parts to the database.
    # part_data: (part_id, part_name, filename, part_other, pn, manuf, oem)
    part_ids = set()
    for item in part_data:
        if item[0] != "NEW":
            part = Part.query.filter_by(part_id=item[0]).first()
            if item[1] != part.name:
                part.name = item[1]
            if item[2] != part.part_img:
                part.part_img = item[2]
            part_ids.add(int(item[0]))
        else:
            if item[1] == "other":
                if Part.query.filter_by(name=item[3]).first() != None:
                    part = Part.query.filter_by(name=item[3]).first()
                    part_ids.add(part.part_id)
                else:
                    part = Part(name=item[3], part_img=item[2])
                    db.session.add(part)
                    db.session.commit()
                    part_num = PartNum(
                            manuf=item[5], part_num=item[4], is_oem_part=item[6], part=part
                        )
                    db.session.add(part_num)
                    part_ids.add(part.part_id)
            else:
                part = Part.query.filter_by(name=item[1]).first()
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
                # create_procedure_part(proc, part)

    # Check all ProcedurePart objects associated with this procedure.
    # If a ProcedurePart object includes a part ID that isn't in part_data,
    # delete that ProcedurePart.
    proc_parts = ProcedurePart.query.filter_by(proc_id=proc.proc_id).all()

    for proc_part in proc_parts:
        if proc_part.part_id not in part_ids:
            db.session.delete(proc_part)

    #############################################################
    ############ TODO: refactor w/o list indexing!! #############
    #############################################################
    # Go through step_data and make sure all step info is updated.
    # Add any new steps to the database.
    # step_data: (step_id, step_order, step_text, step_ref, step_img)

    step_ids = set()
    for item in step_data:
        if item[0] != "NEW":
            step = Step.query.filter_by(step_id=item[0]).first()
            if item[1] != step.order_num:
                step.order_num = item[1]
            if item[2] != step.step_text:
                step.text = item[2]
            if item[3] != step.reference:
                step.reference = item[3]
            if item[4] != step.step_img:
                step.step_img = item[4]
            step_ids.add(int(item[0]))
        else:
            step = Step(
                order_num=item[1],
                step_text=item[2],
                proc=item[3],
                reference=reference,
                step_img=item[4],
            )

            db.session.add(step)
            step_ids.add(new_step.step_id)

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
