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

    # Create test parts.
    part1 = Part(name = 'oil filter', part_img = 'oil_filter.png')
    part2 = Part(name = 'exhaust gasket', part_img = 'exh_gasket.png')
    part3 = Part(name = 'drain plug')
    part4 = Part(name = '10mm bolt', part_img = 'bolt.jpg')
    part5 = Part(name = 'valve cover')
    db.session.add(part1)
    db.session.add(part2)
    db.session.add(part3)
    db.session.add(part4)
    db.session.add(part5)

    db.session.commit()

    # Create test part numbers.
    partnum1 = PartNum(manuf = 'ACDelco', 
                        part_num = '123456',
                        is_oem_part = True,
                        part = part1)
    partnum2 = PartNum(manuf = 'Delphi', 
                        is_oem_part = False,
                        part = part1)
    partnum3 = PartNum(part_num = '7891011',
                        is_oem_part = True,
                        part = part3)
    partnum4 = PartNum(is_oem_part = True,
                        part = part4)
    partnum5 = PartNum(manuf = 'ACDelco', 
                        part_num = '12131415',
                        part = part5)
    db.session.add(partnum1)
    db.session.add(partnum2)
    db.session.add(partnum3)
    db.session.add(partnum4)
    db.session.add(partnum5)

    db.session.commit()

 
    


        
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