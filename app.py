from flask_restful import Api
from endpoints import create_app

APP = create_app()
api = Api(APP)
api.prefix = '/api/v1'

from endpoints.routers.transaction.view import record, credit, debit
from endpoints.routers.admin.view import admin_register, admin_login
from endpoints.routers.customer.view import customer
from endpoints.routers.task.view import task

# Blueprint of app
api.add_resource(record, '/transaction/record/<string:customer_name>')
api.add_resource(credit, '/transaction/credit')
api.add_resource(debit, '/transaction/debit')
api.add_resource(admin_register, '/admin/register')
api.add_resource(admin_login, '/admin/login')
api.add_resource(customer, '/customer', '/customer/<string:customer_name>')
api.add_resource(task, '/task', '/task/<int:task_id>')


if __name__ == '__main__':
    APP.run(host='0.0.0.0')