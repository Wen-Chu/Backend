from flask_restful import Resource, reqparse
from endpoints import DB
from endpoints.routers.admin.model import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

class admin_register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('admin_name', required=True, type=str, help="Admin name cannot be blank.")
        parser.add_argument('password', required=True, type=str, help="Password cannot be blank.")
        args = parser.parse_args()

        try:
            if Admin.query.filter_by(admin_name=args['admin_name']).first():
                return {'error': 'admin_name already exists'}, 400
            hashed_password = generate_password_hash(args['password'], method='pbkdf2')
            new_admin = Admin(admin_name=args['admin_name'], password=hashed_password)
            DB.session.add(new_admin)
            DB.session.commit()
            return {"message": "Registered successfully"}, 200
        except Exception as e:
            return {'error': f'Error processing request: {str(e)}'}, 500

class admin_login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('admin_name', required=True, type=str, help="Admin name cannot be blank.")
        parser.add_argument('password', required=True, type=str, help="Password cannot be blank.")
        args = parser.parse_args()

        try:
            admin_obj = Admin.query.filter_by(admin_name=args['admin_name']).first()
            if admin_obj is None or not check_password_hash(admin_obj.password, args['password']):
                return {'error': 'Invalid admin_name or password'}, 401
            access_token = create_access_token(identity=admin_obj.admin_name)
            return {'access_token': access_token}, 200
        except Exception as e:
            return {'error': f'Error processing request: {str(e)}'}, 500
