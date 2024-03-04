import unittest
from flask_migrate import upgrade, downgrade
from endpoints import DB
from app import APP
from endpoints.routers.customer.model import Customer
from endpoints.routers.admin.model import Admin
from endpoints.routers.transaction.model import Transaction
from datetime import datetime

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
            DB.session.query(Transaction).delete()
            DB.session.commit()

    def add_customer(self, auth_token=None):
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        return self.client.post('/api/v1/customer',
                                json={'customer_name': 'testname', 'balance': 50},
                                headers=headers)

    def credit(self, auth_token=None):
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        return self.client.post('/api/v1/transaction/credit',
                                json={'customer_name': 'testname', 'amount': 20},
                                headers=headers), datetime.now()

    def debit(self, auth_token=None):
        headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        return self.client.post('/api/v1/transaction/debit',
                                json={'customer_name': 'testname', 'amount': 50},
                                headers=headers), datetime.now()

    def test_record(self):
        self.add_customer(self.auth_token)
        _, credit_time = self.credit(self.auth_token)
        _, debit_time = self.debit(self.auth_token)
        response = self.client.get('/api/v1/transaction/record/testname',
                                   headers={'Authorization': f'Bearer {self.auth_token}'})
        transactions = response.get_json()
        credit_transaction = transactions[0]
        debit_transaction = transactions[1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(credit_transaction['customer_id'], 1)
        self.assertEqual(credit_transaction['trans_type'], 'credit')
        self.assertEqual(credit_transaction['amount'], 20)
        self.assertEqual(credit_transaction['balance'], 70)
        self.assertEqual(debit_transaction['trans_type'], 'debit')
        self.assertEqual(debit_transaction['amount'], 50)
        self.assertEqual(debit_transaction['balance'], 20)
        self.assertIsInstance(debit_transaction['timestamp'], str)

    def test_record_customer_not_found(self):
        response = self.client.get('/api/v1/transaction/record/testname',
                                   headers={'Authorization': f'Bearer {self.auth_token}'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Customer not found'})

    def test_credit(self):
        self.add_customer(self.auth_token)
        response, _ = self.credit(self.auth_token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Credited successfully"})


    def test_credit_customer_not_found(self):
        response = self.client.post('/api/v1/transaction/credit',
                                    json={'customer_name': 'testname', 'amount': 50},
                                    headers={'Authorization': f'Bearer {self.auth_token}'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Customer not found'})

    def test_debit(self):
        self.add_customer(self.auth_token)
        response, _ = self.debit(self.auth_token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Debited successfully"})

    def test_debit_customer_not_found(self):
        response = self.client.post('/api/v1/transaction/debit',
                                    json={'customer_name': 'testname', 'amount': 50},
                                    headers={'Authorization': f'Bearer {self.auth_token}'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Customer not found'})

    def test_debit_insufficient_balance(self):
        self.add_customer(self.auth_token)
        response, _ = self.debit(self.auth_token)
        response, _ = self.debit(self.auth_token)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Insufficient balance'})

if __name__ == '__main__':
    unittest.main()