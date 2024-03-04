import unittest
from flask_migrate import upgrade, downgrade
from endpoints import DB
from app import APP
from endpoints.routers.admin.model import Admin

class AdminTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = APP
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            upgrade()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            DB.session.remove()
            downgrade()

    def tearDown(self):
        with self.app.app_context():
            DB.session.query(Admin).delete()
            DB.session.commit()

    def signup_admin(self):
        return self.client.post('/api/v1/admin/register',
                         json={'admin_name': 'testadmin', 'password': 'testpassword'})

    def test_admin_register(self):
        response = self.signup_admin()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Registered successfully'})

    def test_admin_register_invalid(self):
        response = self.client.post('/api/v1/admin/register',
                                    json={'admin_name': 'testadmin'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': {'password': 'Password cannot be blank.'}})

    def test_admin_register_duplicate(self):
        self.signup_admin()
        response = self.signup_admin()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'admin_name already exists'})

    def test_admin_login(self):
        self.signup_admin()
        response = self.client.post('/api/v1/admin/login',
                                    json={'admin_name': 'testadmin', 'password': 'testpassword'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue('access_token' in response.get_json())

    def test_admin_login_invalid(self):
        self.signup_admin()
        response = self.client.post('/api/v1/admin/login',
                                    json={'admin_name': 'testadmin2', 'password': 'testpassword2'})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'error': 'Invalid admin_name or password'})

if __name__ == '__main__':
    unittest.main()