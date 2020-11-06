import os
from random import randint, choice

import crud
import model
import server

# Drop and re-create the database.
os.system('dropdb shopcat')
os.system('createdb shopcat')

# Connect to the database.
# Imported from model.py
model.connect_to_db(server.app)
model.db.create_all()

# Create a set of 10 test tools.
toolbox = []

for tool in range(10):
    
    name = f'tool_{tool}'
    description = 'placeholder'
    tool_img = f'path_{tool}'

    tool = crud.create_tool(name, description, tool_img)
    toolbox.append(tool)

# Create a set of 50 test parts.
parts_bin = []

for part in range(50):
    
    name = f'part_{part}'
    part_img = f'path_{part}'

    part = crud.create_part(name, part_img)
    parts_bin.append(part)

    manuf = choice(['ACDelco', 'Delphi', 'Bosch', 'Continental'])
    part_num = '1234ABCD'
    is_oem_part = True
    part = part

    part_num = crud.create_part_num(manuf, part_num, is_oem_part, part)
    
# Create a set of 10 test cars.
garage = []

for car in range(10):
    
    model = 'Chevrolet'
    make = f'car_{car}'
    model_year = randint(1956, 2020)

    car = crud.create_car(model, make, model_year)
    garage.append(car)

# Create 5 dummy test users.
for user in range(5):
    username = f'user{user}'
    password = f'password{user}'
    nickname = f'nickname{user}'
    avatar_img_url = f'urlpath{user}'
    
    user = crud.create_user(username, password, nickname, avatar_img_url)
    
    for x in range(3):

        # Create 3 pages for each new user.
        size = 99.999
        page_url = f'url_{user.user_id}_{x}'
        page_type = "procedure"

        page = crud.create_page(size, page_url, page_type)

        # Create 3 procedures for each new user.
        title = f'title{user.user_id}_{x}'
        description = f'description{user.user_id}_{x}'
        label = f'label{user.user_id}_{x}'
        img = f'img{user.user_id}_{x}'

        procedure = crud.create_procedure(title, description, label, img, user, page)

        # Randomly assign a car from the garage to each procedure.
        car_num = randint(0, 9)
        proc_car = crud.create_procedure_car(procedure, garage[car_num])

        # Randomly assign up to 3 tools from the existing set 
        # to each of the procedures.
        nums_used = set()
        for x in range(3):
            num = randint(0, 9)
            nums_used.add(num)
        for num in nums_used:
            tool = toolbox[num]
            proc_tool = crud.create_procedure_tool(procedure, tool)
        
        # Randomly assign up to 3 parts from the existing set 
        # to each of the procedures.
        nums_used = set()
        for x in range(3):
            num = randint(0, 49)
            nums_used.add(num)
        for num in nums_used:
            part = parts_bin[num]
            proc_part = crud.create_procedure_part(procedure, part)




