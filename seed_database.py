import os

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

# Create 10 dummy test users.

for user in range(5):
    username = f'user{user}'
    password = f'password{user}'
    nickname = f'nickname{user}'
    avatar_img_url = f'urlpath{user}'
    
    user = crud.create_user(username, password, nickname, avatar_img_url)
    
    for x in range(3):

        # Create 5 pages for each new user.
        size = 99.999
        page_url = f'url_{user.user_id}_{x}'
        page_type = "procedure"

        page = crud.create_page(size, page_url, page_type)

        # Create 5 procedures for each new user.
        title = f'title{user.user_id}_{x}'
        description = f'description{user.user_id}_{x}'
        label = f'label{user.user_id}_{x}'
        img = f'img{user.user_id}_{x}'

        procedure = crud.create_procedure(title, description, label, img, user, page)

