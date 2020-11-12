import unittest
from server import app
from model import db, connect_to_db

class FlaskTests(unittest.TestCase):
    """Tests for the Shop Cat site."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    # def tearDown(self):
        """Stuff to do after each test."""
    
    def test_shopcat_root_route(self):
        """Check that the shopcat root route is rendering properly."""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/new-user" method="POST">', result.data)

if __name__ == "__main__":
    unittest.main()