import os
from random import randint, choice

import crud
import model
from model import db, connect_to_db, User, Procedure, Car, Part, Tool, Step
from model import PartNum, ProcedureCar, ProcedurePart, ProcedureTool
import server
import json

# Drop and re-create the database.
os.system("dropdb shopcat")
os.system("createdb shopcat")
model.connect_to_db(server.app)
model.db.create_all()

# Create a set of tools using info in tools.json.
toolbox = []

with open('data/tools.json') as filename:
    tools_json = json.loads(filename.read())

for tool_json in tools_json:

    name = tool_json
    tool_img = "toolbox.png"
    tool = Tool(name = name, tool_img = tool_img)
    db.session.add(tool)
    toolbox.append(tool)

# Create a set of 50 test parts.
parts_bin = []

for part in range(50):

    name = f"part_{part}"
    part_img = "toolbox.png"

    part = Part(name = name, part_img = part_img)
    db.session.add(part)
    parts_bin.append(part)

    manuf = choice(["ACDelco", "Delphi", "Bosch", "Continental"])
    part_num = "1234ABCD"
    is_oem_part = True
    part = part

    part_num = PartNum(manuf = manuf, part_num = part_num, is_oem_part = is_oem_part, part = part)
    db.session.add(part_num)

# Create a set of 10 test cars.
garage = []

for car in range(10):

    model = f"car_{car}"
    make = "CHEVROLET"
    model_year = randint(1956, 2020)

    car = Car(model = model, make = make, model_year = model_year)
    db.session.add(car)
    garage.append(car)

# Create 5 test users.
for user in range(5):
    username = f"user{user}"
    password = f"password{user}"
    nickname = f"nickname{user}"
    avatar_img_url = "cat.jpg"

    user = User(username = username, password = password, nickname = nickname, avatar_img_url = avatar_img_url)
    db.session.add(user)
    db.session.commit()
    
    for x in range(3):

        # Create 3 procedures for each new user.
        title = f"title{user.user_id}_{x}"
        label = f"label{user.user_id}_{x}"

        procedure = Procedure(title = title, label = label, user = user)
        db.session.add(procedure)
        db.session.commit()

        # Randomly assign a car from the garage to each procedure.
        car_num = randint(0, 9)
        proc_car = ProcedureCar(proc = procedure, car = garage[car_num])
        db.session.add(proc_car)

        # Randomly assign up to 5 tools from the existing set
        # to each procedure.
        nums_used = set()
        for x in range(5):
            num = randint(0, len(toolbox))
            nums_used.add(num)

        for num in nums_used:
            tool = toolbox[num]
            proc_tool = ProcedureTool(proc = procedure, tool = tool)
            db.session.add(proc_tool)

        # Randomly assign up to 3 parts from the existing set
        # to each procedure.
        nums_used = set()
        for x in range(3):
            num = randint(0, 49)
            nums_used.add(num)
        for num in nums_used:
            part = parts_bin[num]
            proc_part = ProcedurePart(proc = procedure, part = part)
            db.session.add(proc_part)

        # Create 3 Steps for each Procedure.
        step1 = Step(
            order_num = 1,
            step_text = f"Procedure_{procedure.proc_id}_step1",
            proc = procedure,
            reference = "No Ref Provided",
            step_img = "toolbox.png",
        )
        step2 = Step(
            order_num = 2,
            step_text = f"Procedure_{procedure.proc_id}_step2",
            proc = procedure,
            reference = "No Ref Provided",
            step_img = "toolbox.png",
        )
        step3 = Step(
            order_num = 3,
            step_text = f"Procedure_{procedure.proc_id}_step3",
            proc = procedure,
            reference = "No Ref Provided",
            step_img = "toolbox.png",
        )
        db.session.add(step1)
        db.session.add(step2)
        db.session.add(step3)

db.session.commit()