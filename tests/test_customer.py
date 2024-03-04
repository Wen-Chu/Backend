import unittest
from flask_migrate import upgrade, downgrade
from endpoints import DB
from app import APP
from endpoints.routers.customer.model import Customer
from endpoints.routers.admin.model import Admin

class CustomerTestCase(unittest.TestCase):
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

    def setUp(self):
        self.client.post('/api/v1/admin/register',
                         json={'admin_name': 'testadmin', 'password': 'testpassword'})
        login_response = self.client.post('/api/v1/admin/login',
                                          json={'admin_name': 'testadmin', 'password': 'testpassword'})
        self.auth_token = login_response.get_json()['access_token']

    def tearDown(self):
        with self.app.app_context():
            DB.session.query(Customer).delete()
            DB.session.query(Admin).delete()
            DB.session.commit()

    def add_customer(self, auth_token=None):
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        return self.client.post('/api/v1/customer',
                                json={'customer_name': 'testname', 'balance': 100},
                                headers=headers)
        return response

    def test_get_customer(self):
        self.add_customer(self.auth_token)
        response = self.client.get('/api/v1/customer/testname',
                                   headers={'Authorization': f'Bearer {self.auth_token}'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 1, 'customer_name': 'testname', 'balance': 100})

    def test_notfound_customer(self):
        response = self.client.get('/api/v1/customer/testname',
                                   headers={'Authorization': f'Bearer {self.auth_token}'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Customer not found'})

    def test_add_customer(self):
        response = self.add_customer(self.auth_token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Customer created successfully'})

if __name__ == '__main__':
    unittest.main()