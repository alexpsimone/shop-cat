"""
Routes covered by this file:
/
/dashboard/<user_id>
/edit-procedure/<proc_id>
/existing-user
/home
/login
/new-user
/procedure/<proc_id>
/tool/<tool_id>
/vehicle/<make>
/vehicle/<make>/<model_year>
/vehicle/<make>/<model_year>/<model>
/write-procedure

Routes not fully covered by this file:
/build-procedure <---written but not working
/get-models.json <---written but not working
/get-parts.json
/get-tools.json
/rebuild-procedure
/uploads/<filename>
/vehicle-select.json
any redirects when user not in session
"""

import unittest
from crud import app
from model import db, connect_to_db, User, Procedure, Car, Part, Tool, Step
from model import PartNum, ProcedureCar, ProcedurePart, ProcedureTool
import os
from seed_testdb import load_all

# Drop and re-create the test database.
os.system("dropdb testdb")
os.system("createdb testdb")

class FlaskTests(unittest.TestCase):
    """Tests for the Shop Cat site."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_dashboard_no_session_redirect(self):
        """Check that the user dashboard redirects if no user in session."""

        result = self.client.get(f"/dashboard/1", follow_redirects = True)
        self.assertEqual(result.status_code, 200)
    
    def test_edit_proc_no_session_redirect(self):
        """Check that /edit-procedure redirects if no user in session."""

        result = self.client.get(f"/edit-procedure/1", follow_redirects = True)
        self.assertEqual(result.status_code, 200)

    def test_home_redirect(self):
        """Check that the home route redirects with no session."""
        
        result = self.client.get("/home", follow_redirects = True)
        self.assertEqual(result.status_code, 200)

    def test_login_route(self):
        """Check that the login route renders properly."""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/existing-user"', result.data)
        self.assertNotIn(b'<form action="/new-user"', result.data)
    
    def test_shopcat_root_route(self):
        """Check that the shopcat root route is rendering properly."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/new-user" method="POST">', result.data)
        self.assertNotIn(b'<form action="/existing-user"', result.data)


class ShopCatTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "key"
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb")
        db.create_all()
        load_all()

        # Put user1 into session.
        with self.client as c:
            with c.session_transaction() as sess:
                sess["current_user"] = 1
                sess["model_year"] = 2011
                sess["make"] = "CHEVROLET"
                sess["model"] = "Cruze"

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_build_procedure(self):
        """Check that the build-procedure route processes properly."""

        result = self.client.post(
            "/build-procedure",
            data={
                'proc_title': 'new_title',
                'proc_label': 'new_label',
                'NUM_STEPS': '1',
                'NUM_TOOLS': '1',
                'NUM_PARTS': '1',
                'step_text_1': 'step 1 text',
                'ref_1': 'True',
                'step_img_1': 'cat.png',
                'ref_text_1': 'https://google.com',
                'tool_req_1': 'screwdriver',
                'tool_other_1': None,
                'tool_img_1': None,
                'part_req_1': 'oil filter',
                'part_img_1': None,
                'part_1_other_name': None,
                'part_1_other_num': None,
                'part_1_other_manuf': None,
                'oem_1': 'True',
            },
            follow_redirects = True,
        )
        self.assertEqual(result.status_code, 200)

    def test_edit_procedure(self):
        """Check that the edit-procedure route processes properly."""

        procedures = Procedure.query.all()

        for procedure in procedures:
            result = self.client.get(f"/edit-procedure/{procedure.proc_id}")
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<button id="car-add">Add a Vehicle', result.data)

    def test_existing_user_route_correct_pass(self):
        """Check that the login route works properly with the correct password filled in."""

        result = self.client.post(
            "/existing-user",
            data={"username": "username1", "password": "pass1"},
            follow_redirects=True,
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Browse all the available procedures:", result.data)

    def test_existing_user_route_wrong_pass(self):
        """Check that the login route works properly with the wrong password filled in."""

        result = self.client.post(
            "/existing-user",
            data={"username": "username1", "password": "pass3"},
            follow_redirects=True,
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Password is incorrect.", result.data)
    
    def test_get_models_json_route(self):
        """Confirm that the get-models.json query works."""

        result = self.client.get(
            "/get-models.json",
            data={"modelYear": 2005, "make": 'HONDA'},
            follow_redirects=True,
        )
        self.assertEqual(result.status_code, 200)

    def test_get_parts_json_route(self):
        """Confirm that the get-parts.json query works."""

        result = self.client.get("/get-parts.json")
        self.assertEqual(result.status_code, 200)
    
    def test_get_tools_json_route(self):
        """Confirm that the get-parts.json query works."""

        result = self.client.get("/get-tools.json")
        self.assertEqual(result.status_code, 200)

    def test_home_route(self):
        """Check that the home route is rendering properly."""

        result = self.client.get("/home")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Browse all the available procedures:", result.data)

    def test_new_user_route_new(self):
        """Check that the account creation route works properly with new user info."""

        result = self.client.post(
            "/new-user",
            data={
                "username": "usernameA",
                "password": "passA",
                "nickname": "nicknameA",
            },
            follow_redirects=True,
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"New account created.", result.data)
        self.assertNotIn(b"A user already exists", result.data)

    def test_new_user_route_existing(self):
        """Check that the account creation route works properly with exisitng user info."""

        result = self.client.post(
            "/new-user",
            data={
                "username": "username1",
                "password": "pass1",
                "nickname": "nickname1",
            },
            follow_redirects=True,
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"A user already exists", result.data)
        self.assertNotIn(b"New account created.", result.data)

    def test_procedure_by_proc_id_route(self):
        """Check that the procedure view route is rendering properly."""

        all_procedures = Procedure.query.all()

        for procedure in all_procedures:
            result = self.client.get(f"/procedure/{procedure.proc_id}")
            self.assertEqual(result.status_code, 200)
            self.assertIn(b"<p>Here are the steps in the procedure:</p>", result.data)
            self.assertNotIn(b'<form action="/vehicle-select"', result.data)

    def test_tool_route(self):
        """Check that the user dashboard is rendering properly."""

        all_tools = Tool.query.all()
        for tool in all_tools:
            result = self.client.get(f"/tool/{tool.tool_id}")
            self.assertEqual(result.status_code, 200)
            self.assertIn(b"<h1>Information about", result.data)

    def test_user_dashboard_route(self):
        """Check that the user dashboard is rendering properly."""

        all_users = User.query.all()
        for user in all_users:
            result = self.client.get(f"/dashboard/{user.user_id}")
            self.assertEqual(result.status_code, 200)
            self.assertIn(b"""<h2>Procedures you've created:</h2>""", result.data)

    def test_vehicle_make_route(self):
        """Check that the vehicle make link page is rendering properly."""

        first_car = Car.query.first()
        make = first_car.make

        result = self.client.get(f"/vehicle/{make}")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>Model years available for all", result.data)
        self.assertNotIn(b'<form action="/vehicle-select"', result.data)

    def test_vehicle_make_my_route(self):
        """Check that the vehicle model year link page is rendering properly."""

        first_car = Car.query.first()
        make = first_car.make
        model_year = first_car.model_year

        result = self.client.get(f"/vehicle/{make}/{model_year}")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>Models for ", result.data)
        self.assertNotIn(b'<form action="/vehicle-select"', result.data)

    def test_vehicle_make_my_model_route(self):
        """Check that the vehicle model link page is rendering properly."""

        first_car = Car.query.first()
        make = first_car.make
        model_year = first_car.model_year
        model = first_car.model

        result = self.client.get(f"/vehicle/{make}/{model_year}/{model}")
        self.assertEqual(result.status_code, 200)

    def test_write_procedure_route(self):
        """Check that the write-procedure route is rendering properly."""

        result = self.client.get("/write-procedure", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(
            b'<form action="/build-procedure", method="POST", enctype="multipart/form-data">',
            result.data,
        )


if __name__ == "__main__":
    unittest.main()
