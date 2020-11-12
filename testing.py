import unittest
from server import app
from model import db, connect_to_db
import os

# Drop and re-create the test database.
os.system('dropdb testdb')
os.system('createdb testdb')
os.system('python3 seed_testdb.py')


class FlaskTests(unittest.TestCase):
    """Tests for the Shop Cat site."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    
    def test_shopcat_root_route(self):
        """Check that the shopcat root route is rendering properly."""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/new-user" method="POST">', result.data)


class ShopCatTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        
        # Connect to test database
        connect_to_db(app, db_uri = "postgresql:///testdb")
        db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
    

    def test_home_route(self):
        """Check that the home route is rendering properly."""

        result = self.client.get('/home')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Browse all the available procedures:', result.data)
    

    def test_write_procedure_route(self):
        """Check that the write-procedure route is rendering properly."""

        result = self.client.get('/write-procedure')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/build-procedure", method="POST">',
                             result.data)

    #########################################################################
    ### TODO: Add this function, figure out how to incorporate variable route.
    #########################################################################
    
    # def test_procedure_by_proc_id_route(self):
        """Check that the write-procedure route is rendering properly."""


if __name__ == "__main__":
    unittest.main()