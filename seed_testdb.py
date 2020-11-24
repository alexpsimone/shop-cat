from random import randint, choice
from server import app
from model import db, connect_to_db, Car, Part, PartNum, Step, Tool, User
from model import Procedure, ProcedureCar, ProcedurePart, ProcedureTool


def load_all():
    """Load all the things."""

    # Create test users.
    user1 = User(
        username="username1",
        password="pass1",
        nickname="nickname1",
        avatar_img_url="myavatar1.png",
    )
    user2 = User(username="username2", password="pass2", nickname="nickname2")
    user3 = User(username="username3", password="pass3", avatar_img_url="myavatar3.png")
    user4 = User(username="username4", password="pass4")
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)

    # Create test cars.
    car1 = Car(model_year=1999, make="FORD", model="Taurus")

    car2 = Car(model="Impala")
    db.session.add(car1)
    db.session.add(car2)

    # Create test tools.
    tool1 = Tool(name="screwdriver", tool_img="screwdriver.jpg")
    tool2 = Tool(name="wrench", tool_img="wrench.jpg")
    tool3 = Tool(name="hammer")
    db.session.add(tool1)
    db.session.add(tool2)
    db.session.add(tool3)

    # Create test parts.
    part1 = Part(name="oil filter", part_img="oil_filter.png")
    part2 = Part(name="exhaust gasket", part_img="exh_gasket.png")
    part3 = Part(name="drain plug")
    part4 = Part(name="10mm bolt", part_img="bolt.jpg")
    part5 = Part(name="valve cover")
    db.session.add(part1)
    db.session.add(part2)
    db.session.add(part3)
    db.session.add(part4)
    db.session.add(part5)

    db.session.commit()

    # Create test part numbers.
    partnum1 = PartNum(manuf="ACDelco", part_num="123456", is_oem_part=True, part=part1)
    partnum2 = PartNum(manuf="Delphi", is_oem_part=False, part=part1)
    partnum3 = PartNum(part_num="7891011", is_oem_part=True, part=part3)
    partnum4 = PartNum(is_oem_part=True, part=part4)
    partnum5 = PartNum(manuf="ACDelco", part_num="12131415", part=part5)
    db.session.add(partnum1)
    db.session.add(partnum2)
    db.session.add(partnum3)
    db.session.add(partnum4)
    db.session.add(partnum5)

    db.session.commit()

    # Create test procedures.
    procedure1 = Procedure(title="Oil Change", label="basic care", user=user1)
    procedure2 = Procedure(title="Tire Rotation", label="basic care", user=user2)
    procedure3 = Procedure(title="Engine Swap", label="major overhaul", user=user3)
    procedure4 = Procedure(
        title="Exhaust Gasket Replacement", label="old car care", user=user4
    )
    db.session.add(procedure1)
    db.session.add(procedure2)
    db.session.add(procedure3)
    db.session.add(procedure4)

    db.session.commit()

    # Add a Step object for each Procedure.
    step1 = Step(
        order_num=1,
        reference="http://www.google.com",
        step_text="Here is some text.",
        proc=procedure1,
        step_img="toolbox.jpg",
    )
    step2 = Step(
        order_num=1,
        step_text="Here is some text.",
        proc=procedure2,
        step_img="toolbox.jpg",
    )
    step3 = Step(
        order_num=1,
        step_text="Here is some text.",
        proc=procedure3,
        step_img="toolbox.jpg",
    )
    step4 = Step(
        order_num=1,
        reference="http://www.google.com",
        step_text="Here is some text.",
        proc=procedure4,
    )
    db.session.add(step1)
    db.session.add(step2)
    db.session.add(step3)
    db.session.add(step4)

    # Add a Car to each Procedure by creating a ProcedureCar object.
    proc_car_1 = ProcedureCar(proc=procedure1, car=car1)
    proc_car_2 = ProcedureCar(proc=procedure2, car=car1)
    proc_car_3 = ProcedureCar(proc=procedure3, car=car2)
    proc_car_4 = ProcedureCar(proc=procedure4, car=car2)
    db.session.add(proc_car_1)
    db.session.add(proc_car_2)
    db.session.add(proc_car_3)
    db.session.add(proc_car_4)

    # Add a Part to most Procedures by creating ProcedurePart objects.
    proc_part_1 = ProcedurePart(proc=procedure1, part=part1)
    proc_part_2 = ProcedurePart(proc=procedure1, part=part2)
    proc_part_3 = ProcedurePart(proc=procedure1, part=part3)
    proc_part_4 = ProcedurePart(proc=procedure2, part=part1)
    proc_part_5 = ProcedurePart(proc=procedure2, part=part4)
    proc_part_6 = ProcedurePart(proc=procedure2, part=part3)
    db.session.add(proc_part_1)
    db.session.add(proc_part_2)
    db.session.add(proc_part_3)
    db.session.add(proc_part_4)
    db.session.add(proc_part_5)
    db.session.add(proc_part_6)

    # Add a Tool to most Procedures by creating ProcedureTool objects.
    proc_tool_1 = ProcedureTool(proc=procedure1, tool=tool1)
    proc_tool_2 = ProcedureTool(proc=procedure1, tool=tool2)
    proc_tool_3 = ProcedureTool(proc=procedure1, tool=tool3)
    proc_tool_4 = ProcedureTool(proc=procedure3, tool=tool1)
    proc_tool_5 = ProcedureTool(proc=procedure3, tool=tool2)
    proc_tool_6 = ProcedureTool(proc=procedure3, tool=tool3)
    db.session.add(proc_tool_1)
    db.session.add(proc_tool_2)
    db.session.add(proc_tool_3)
    db.session.add(proc_tool_4)
    db.session.add(proc_tool_5)
    db.session.add(proc_tool_6)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app, db_uri="postgresql:///testdb")
    print("Connected to testdb.")
    db.create_all()
    load_all()
