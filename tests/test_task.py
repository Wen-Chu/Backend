import unittest
from flask_migrate import upgrade, downgrade
from endpoints import DB
from app import APP
from endpoints.routers.admin.model import Admin
from endpoints.routers.task.model import Task

class TaskTestCase(unittest.TestCase):
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
            DB.session.query(Admin).delete()
            DB.session.query(Task).delete()
            DB.session.commit()

    def add_task(self, task_name="test_task", status=0):
        return self.client.post('/api/v1/task',
                                json={'task_name': task_name, 'status': status},
                                headers={'Authorization': f'Bearer {self.auth_token}'})

    def get_task(self, task_id=None):
        if task_id:
            url = f'/api/v1/task/{task_id}'
        else:
            url = '/api/v1/task'
        return self.client.get(url, headers={'Authorization': f'Bearer {self.auth_token}'})

    def update_task(self, task_id, task_name="updated_task", status=1):
        return self.client.put('/api/v1/task',
                                json={'task_id': task_id, 'task_name': task_name, 'status': status},
                                headers={'Authorization': f'Bearer {self.auth_token}'})

    def delete_task(self, task_id):
        return self.client.delete(f'/api/v1/task/{task_id}', headers={'Authorization': f'Bearer {self.auth_token}'})

    def test_get_single_task(self):
        self.add_task()
        get_response = self.get_task(1)
        task_data = get_response.get_json()

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(task_data['id'], 1)
        self.assertEqual(task_data['task_name'], 'test_task')
        self.assertEqual(task_data['status'], 0)
        self.assertEqual(task_data['admin_name'], 'testadmin')
        self.assertIsInstance(task_data['created_at'], str)

    def test_get_all_tasks(self):
        self.add_task(task_name="Task 1", status=0)
        self.add_task(task_name="Task 2", status=1)
        get_response = self.get_task()
        tasks = get_response.get_json()

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['task_name'], "Task 1")
        self.assertEqual(tasks[1]['task_name'], "Task 2")
        self.assertIsInstance(tasks[1]['last_updated'], str)

    def test_create_task(self):
        response = self.add_task()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Task created successfully"})

    def test_task_update(self):
        self.add_task()
        update_response = self.update_task(1)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json, {"message": "Task updated successfully"})

    def test_task_deletion(self):
        self.add_task()
        delete_response = self.delete_task(1)

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.json, {"message": "Task deleted successfully"})

    def test_task_not_found(self):
        delete_response = self.delete_task(999)

        self.assertEqual(delete_response.status_code, 404)
        self.assertEqual(delete_response.json, {"error": "Task not found"})


if __name__ == '__main__':
    unittest.main()