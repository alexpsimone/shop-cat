import os

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
for user in range(10):
    username = f'user{user}'
    password = f'password{user}'
    nickname = f'nickname{user}'
    avatar_img_url = f'urlpath{user}'
    