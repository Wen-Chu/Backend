from datetime import datetime
from endpoints import DB
from flask_restful import Resource, reqparse
from endpoints.routers.transaction.model import Transaction
from endpoints.routers.customer.model import Customer
from flask_jwt_extended import jwt_required

class record(Resource):
    @jwt_required()
    def get(self, customer_name):
        try:
            customer_obj = Customer.query.filter_by(customer_name=customer_name).first()
            if not customer_obj:
                return {"error": "Customer not found"}, 404
            transactions = Transaction.query.filter_by(customer_id=customer_obj.id).all()
            if not transactions:
                return {"error": "No transaction found for the given customer_name"}, 404
            transactions_data = [{"id": transaction.id, "customer_id": transaction.customer_id, "trans_type": transaction.trans_type,
                                  "amount": transaction.amount, "balance": transaction.balance,
                                  "timestamp": transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for transaction in transactions]
            return transactions_data, 200
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500
class credit(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('customer_name', required=True, type=str, help="customer_name cannot be blank.")
            parser.add_argument('amount', required=True, type=int, help="Amount cannot be blank.")
            args = parser.parse_args()

            customer_obj = Customer.query.filter_by(customer_name=args['customer_name']).first()
            if customer_obj:
                customer_obj.balance += args['amount']
                DB.session.commit()
                new_transaction = Transaction(customer_id=customer_obj.id, trans_type='credit', amount=args['amount'],
                                              balance=customer_obj.balance, timestamp=datetime.now())
                DB.session.add(new_transaction)
                DB.session.commit()
                return {"message": "Credited successfully"}, 200
            else:
                return {"error": "Customer not found"}, 404
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500

class debit(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('customer_name', required=True, type=str, help="customer_name cannot be blank.")
            parser.add_argument('amount', required=True, type=int, help="Amount cannot be blank.")
            args = parser.parse_args()

            customer_obj = Customer.query.filter_by(customer_name=args['customer_name']).first()
            if customer_obj:
                if customer_obj.balance < args['amount']:
                    return {"error": "Insufficient balance"}, 400

                customer_obj.balance -= args['amount']
                DB.session.commit()
                new_transaction = Transaction(customer_id=customer_obj.id, trans_type='debit', amount=args['amount'],
                                              balance=customer_obj.balance, timestamp=datetime.now())
                DB.session.add(new_transaction)
                DB.session.commit()
                return {"message": "Debited successfully"}, 200
            else:
                return {"error": "Customer not found"}, 404
        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}, 500