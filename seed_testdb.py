from random import randint, choice
from server import app
from model import db, connect_to_db, User, Car, Part, Tool, Procedure

import crud

def load_all():
    """Load all the things."""

    # Create test users.
    user1 = User(username = 'username1',
                    password = 'pass1',
                    nickname = 'nickname1',
                    avatar_img_url = 'myavatar1.png')
    user2 = User(username = 'username2',
                    password = 'pass2',
                    nickname = 'nickname2')
    user3 = User(username = 'username3',
                    password = 'pass3',
                    avatar_img_url = 'myavatar3.png')
    user4 = User(username = 'username4', 
                    password = 'pass4')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)

    # Create test cars.
    car1 = Car(model_year = 1999,
                make = 'FORD',
                model = 'Taurus')
    
    car2 = Car(model = 'Impala')
    db.session.add(car1)
    db.session.add(car2)

    # Create test tools.
    tool1 = Tool(name = 'screwdriver', tool_img = 'screwdriver.jpg')
    tool2 = Tool(name = 'wrench', tool_img = 'wrench.jpg')
    tool3 = Tool(name = 'hammer')
    db.session.add(tool1)
    db.session.add(tool2)
    db.session.add(tool3)

    db.session.commit()





    # # Create a set of 10 test tools.
    # toolbox = []

    # for tool in range(5):
        
    #     name = f'tool_{tool}'
    #     tool_img = f'path_{tool}'

    #     tool = crud.create_tool(name, tool_img)
    #     toolbox.append(tool)

    # # Create a set of 50 test parts.
    # parts_bin = []

    # for part in range(10):
        
    #     name = f'part_{part}'
    #     part_img = f'path_{part}'

    #     part = crud.create_part(name, part_img)
    #     parts_bin.append(part)

    #     manuf = choice(['ACDelco', 'Delphi', 'Bosch', 'Continental'])
    #     part_num = '1234ABCD'
    #     is_oem_part = True
    #     part = part

    #     part_num = crud.create_part_num(manuf, part_num, is_oem_part, part)
        
    # # Create a set of 10 test cars.
    # garage = []

    # for car in range(5):
        
    #     model = f'car_{car}'
    #     make = 'Chevrolet'
    #     model_year = randint(1956, 2020)

    #     car = crud.create_car(model, make, model_year)
    #     garage.append(car)

    # # Create 5 test users.
    # for user in range(5):
    #     username = f'user{user}'
    #     password = f'password{user}'
    #     nickname = f'nickname{user}'
    #     avatar_img_url = f'urlpath{user}'
        
    #     user = crud.create_user(username, password, nickname, avatar_img_url)
        
    #     for x in range(3):

    #         # Create 3 procedures for each new user.
    #         title = f'title{user.user_id}_{x}'
    #         description = f'description{user.user_id}_{x}'
    #         label = f'label{user.user_id}_{x}'
    #         img = 'nopath'

    #         procedure = crud.create_procedure(title, description, label, img, user)

    #         # Randomly assign a car from the garage to each procedure.
    #         car_num = randint(0, 4)
    #         proc_car = crud.create_procedure_car(procedure, garage[car_num])

    #         # Randomly assign up to 3 tools from the existing set 
    #         # to each procedure.
    #         nums_used = set()
    #         for x in range(3):
    #             num = randint(0, 4)
    #             nums_used.add(num)
    #         for num in nums_used:
    #             tool = toolbox[num]
    #             proc_tool = crud.create_procedure_tool(procedure, tool)
            
    #         # Randomly assign up to 3 parts from the existing set 
    #         # to each procedure.
    #         nums_used = set()
    #         for x in range(3):
    #             num = randint(0, 9)
    #             nums_used.add(num)
    #         for num in nums_used:
    #             part = parts_bin[num]
    #             proc_part = crud.create_procedure_part(procedure, part)


if __name__ == '__main__':
    connect_to_db(app)
    print("Connected to testdb.")
    db.create_all()
    load_all()