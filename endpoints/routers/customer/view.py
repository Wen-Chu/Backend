from flask_restful import Resource, reqparse
from endpoints.routers.customer.model import Customer
from flask_jwt_extended import jwt_required
from endpoints import DB

class customer(Resource):
    @jwt_required()
    def get(self, customer_name=None):
        try:
            if not customer_name:
                customers = Customer.query.all()
                if len(customers) == 0:
                    return {"error": "No customer"}, 404
                customer_data = []
                for customer in customers:
                    customer_data.append(
                        {"id": customer.id, "customer_name": customer.customer_name, "balance": customer.balance})
            else:
                customer_obj = Customer.query.filter_by(customer_name=customer_name).first()
                if not customer_obj:
                    return {"error": "Customer not found"}, 404
                customer_data = {"id": customer_obj.id, "customer_name": customer_obj.customer_name, "balance": customer_obj.balance}
            return customer_data, 200
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500

    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('customer_name', required=True, type=str, help="customer_name cannot be blank.")
            parser.add_argument('balance', required=True, type=int, help="Balance cannot be blank.")
            args = parser.parse_args()
            new_customer = Customer(customer_name=args['customer_name'], balance=args['balance'])
            DB.session.add(new_customer)
            DB.session.commit()
            return {"message": "Customer created successfully"}, 200
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500