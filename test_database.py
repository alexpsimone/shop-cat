import os

import crud
import model
import server

# Drop and re-create a testing database.
os.system("dropdb testing_db")
os.system("createdb testing_db")
model.connect_to_db(server.app)
model.db.create_all()

# Create new tools.
test_tool_1_name = "test_tool_1"
test_tool_1_img = "test_tool_1_img.jpg"
