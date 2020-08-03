import sqlite3
from datetime import date

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.policy import PolicyModel
from resources.user import today


class PolicyRegister(Resource):
    TABLE_NAME = 'policy'

    parser = reqparse.RequestParser()

    parser.add_argument('policy_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('start_date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('duration_in_years',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('company_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('initial_deposit',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('policy_type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('user_type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('terms_per_year',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('term_amount',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('interest',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, policy_name):
        policy = PolicyModel.find_by_policy_name(policy_name)
        if policy:
            return policy.json()
        return {'message': 'policy not found'}, 404

    @jwt_required()
    def get(self, company_name):
        policy = PolicyModel.find_by_company_name(company_name)
        if policy:
            return policy.json()
        return {'message': 'policy not found'}, 404


    @jwt_required
    def get_type(self, policy_type):
        policy = PolicyModel.find_by_policy_type(policy_type)
        if policy:
            return policy.json()
        return {'message': 'policy not found'}, 404

    @jwt_required
    def get_type(self, policy_id):
        policy = PolicyModel.find_by_policy_id(policy_id)
        if policy:
            return policy.json()
        return {'message': 'policy not found'}, 404

    @jwt_required
    def get_years(self, duration_in_years):
        policy = PolicyModel.find_by_years(duration_in_years)
        if policy:
            return policy.json()
        return {'message': 'policy not found'}, 404

    def post(self):
        data = PolicyRegister.parser.parse_args()

        connection = sqlite3.connect('data.db')
        print(data['policy_type'])
        cursor = connection.cursor()
        if data['policy_type'] == 'Vehicle Insurance':
            policy_type_id = 'VI'
        elif data['policy_type'] == 'Travel Insurance':
            policy_type_id = 'TI'
        elif data['policy_type'] == 'Health Insurance':
            policy_type_id = 'HI'
        elif data['policy_type'] == 'Life Insurance':
            policy_type_id = 'LI'
        elif data['policy_type'] == 'Child Plans':
            policy_type_id = 'CP'
        elif data['policy_type'] == 'Retirement Plans':
            policy_type_id = 'RT'
        print(type(policy_type_id))
        i = 1
        #while i > 0:
        num = 4 + i
        i = i+1


        year_of_start_date = today.strftime("%Y")
        print(type(year_of_start_date))
        policy_id = policy_type_id + '-' + year_of_start_date + '-' + '00' + str(num)
        x = int(data['duration_in_years'])*int(data['terms_per_year'])*int(data['term_amount'])
        y = int(data['interest'])/100
        maturity_amount = int(data['initial_deposit'])+x+(x*y)
        print(maturity_amount)
        query = "INSERT INTO {table} VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['policy_name'], data['start_date'], data['duration_in_years'], data['company_name'], data['initial_deposit'], data['policy_type'], data['user_type'], data['terms_per_year'], data['term_amount'], data['interest'],maturity_amount, policy_id))
        connection.commit()
        connection.close()

        return {"message": "Policy created successfully."}, 201


class PolicyList(Resource):
    def get(self):
        return {'policies': list(map(lambda x: x.json(), PolicyModel.query.all()))}


