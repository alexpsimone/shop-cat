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

with open("data/tools.json") as filename:
    tools_json = json.loads(filename.read())

for tool_json in tools_json:

    name = tool_json
    tool_img = "toolbox.png"
    tool = Tool(name=name, tool_img=tool_img)
    db.session.add(tool)
    toolbox.append(tool)

# Create a set of 50 test parts.
parts_bin = []

with open("data/parts.json") as filename:
    parts_json = json.loads(filename.read())

for part_json in parts_json:

    name = part_json
    part_img = "toolbox.png"

    part = Part(name=name, part_img=part_img)
    db.session.add(part)
    parts_bin.append(part)

    manuf = choice(["ACDelco", "Delphi", "Bosch", "Continental"])
    part_num = "1234ABCD"
    is_oem_part = True
    part = part

    part_num = PartNum(
        manuf=manuf, part_num=part_num, is_oem_part=is_oem_part, part=part
    )
    db.session.add(part_num)

# Create a set of 10 test cars.
garage = []

makes = crud.get_all_rockauto_makes()

for car in range(10):

    make = choice(makes)
    model_years = crud.get_all_rockauto_model_years(make)
    model_year = choice(model_years)
    models = crud.get_all_rockauto_models(make, model_year)
    model = choice(models)

    car = Car(model=model, make=make, model_year=model_year)
    db.session.add(car)
    garage.append(car)

# Create 5 test users.
with open("data/users.json") as filename_1:
    users_json = json.loads(filename_1.read())

with open("data/procedures.json") as filename_2:
    procs_json = json.loads(filename_2.read())

for user_json in users_json:

    username = user_json["username"]
    password = "pass"
    nickname = user_json["nickname"]
    avatar_img_url = "cat.jpg"

    user = User(
        username=username,
        password=password,
        nickname=nickname,
        avatar_img_url=avatar_img_url,
    )
    db.session.add(user)
    db.session.flush()

    for x in range(3):

        # Create 3 procedures for each new user.
        proc_json = choice(procs_json)
        title = proc_json["title"]
        label = proc_json["label"]

        procedure = Procedure(title=title, label=label, user=user)
        db.session.add(procedure)
        db.session.flush()

        # Create 3 Steps for each Procedure.

        possible_imgs = [
            "demo_1.jpg",
            "demo_2.jpg",
            "demo_3.jpg",
            "demo_4.jpg",
            "demo_5.jpg",
            "heater_core_1.PNG",
            "heater_core_4.PNG",
            "heater_core_5.PNG",
            "heater_core_6.PNG",
            "heater_core_9.PNG",
        ]
        possible_videos = [
            "n4vusY2-rkQ",
            "I-ZNBaZbNF4",
            "oWqZQX0HvTQ",
            "UyG-wpTbZDI",
            "25gYezR_k6c",
        ]

        step1 = Step(
            order_num=1,
            step_text="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
            proc=procedure,
            reference="https://camaro6.com",
            step_img=choice(possible_imgs),
        )
        step2 = Step(
            order_num=2,
            step_text="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
            proc=procedure,
            reference="No Ref Provided",
            step_img=choice(possible_imgs),
        )
        step3 = Step(
            order_num=3,
            step_text="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
            proc=procedure,
            reference=choice(possible_videos),
            step_img=choice(possible_imgs),
        )
        step4 = Step(
            order_num=4,
            step_text="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
            proc=procedure,
            reference="https://ratsun.net",
            step_img=choice(possible_imgs),
        )
        db.session.add(step1)
        db.session.add(step2)
        db.session.add(step3)
        db.session.add(step4)
        db.session.flush()

        # Randomly assign a car from the garage to each procedure.
        car_num = randint(0, 9)
        proc_car = ProcedureCar(proc=procedure, car=garage[car_num])
        db.session.add(proc_car)
        db.session.flush()

        # Randomly assign up to 5 tools from the existing set
        # to each procedure.
        nums_used = set()
        for x in range(5):
            num = randint(0, (len(toolbox) - 1))
            nums_used.add(num)

        for num in nums_used:
            tool = toolbox[num]
            proc_tool = ProcedureTool(proc=procedure, tool=tool)
            db.session.add(proc_tool)
            db.session.flush()

        # Randomly assign up to 3 parts from the existing set
        # to each procedure.
        nums_used = set()
        for x in range(3):
            num = randint(0, 49)
            nums_used.add(num)
        for num in nums_used:
            part = parts_bin[num]
            proc_part = ProcedurePart(proc=procedure, part=part)
            db.session.add(proc_part)
            db.session.flush()


# Seed database with a procedure that's complete enough to share at demo night.
with open("data/gold_proc.json") as filename:
    demo_proc_json = json.loads(filename.read())

print(demo_proc_json)

title = demo_proc_json["title"]
label = demo_proc_json["label"]
user = demo_proc_json["created_by_user_id"]
demo_proc = Procedure(title=title, label=label, created_by_user_id=user)


db.session.add(demo_proc)

model_years = demo_proc_json["model_years"]
make = demo_proc_json["make"]
models = demo_proc_json["models"]

for model_year in model_years[:-1]:
    model = models[0]
    car = Car(model_year=model_year, make=make, model=model)
    db.session.add(car)
    proc_car = ProcedureCar(proc=demo_proc, car=car)
    db.session.add(proc_car)

for model_year in model_years[1:]:
    model = models[1]
    car = Car(model_year=model_year, make=make, model=model)
    db.session.add(car)
    proc_car = ProcedureCar(proc=demo_proc, car=car)
    db.session.add(proc_car)

db.session.flush()

tool1 = Tool(
    name=demo_proc_json["tool_1"]["name"], tool_img=demo_proc_json["tool_1"]["tool_img"]
)
tool2 = Tool(
    name=demo_proc_json["tool_2"]["name"], tool_img=demo_proc_json["tool_2"]["tool_img"]
)
tool3 = Tool(
    name=demo_proc_json["tool_3"]["name"], tool_img=demo_proc_json["tool_3"]["tool_img"]
)
db.session.add(tool1)
db.session.add(tool2)
db.session.add(tool3)
proc_tool_1 = ProcedureTool(proc=demo_proc, tool=tool1)
proc_tool_2 = ProcedureTool(proc=demo_proc, tool=tool2)
proc_tool_3 = ProcedureTool(proc=demo_proc, tool=tool3)
db.session.add(proc_tool_1)
db.session.add(proc_tool_2)
db.session.add(proc_tool_3)

db.session.flush()

part1 = Part(
    name=demo_proc_json["part_1"]["name"], part_img=demo_proc_json["part_1"]["part_img"]
)
part2 = Part(
    name=demo_proc_json["part_2"]["name"], part_img=demo_proc_json["part_2"]["part_img"]
)
db.session.add(part1)
db.session.add(part2)
proc_part_1 = ProcedurePart(proc=demo_proc, part=part1)
proc_part_2 = ProcedurePart(proc=demo_proc, part=part2)
db.session.add(proc_part_1)
db.session.add(proc_part_2)

for count in range(1, 4):
    step_text = demo_proc_json[f"step_{count}"]["step_text"]
    ref_text = demo_proc_json[f"ref_{count}"]
    step_img = None

    [reference, filename] = crud.get_step_ref_and_img(ref_text, step_img)

    new_step = Step(
        order_num=count,
        step_text=step_text,
        proc=demo_proc,
        reference=reference,
        step_img=filename,
    )
    db.session.add(new_step)

for count in range(4, 9):
    step = Step(
        order_num=demo_proc_json[f"step_{count}"]["order_num"],
        step_text=demo_proc_json[f"step_{count}"]["step_text"],
        step_img="toolbox.png",
        reference="No Ref Provided",
        proc=demo_proc,
    )
    db.session.add(step)

db.session.commit()
