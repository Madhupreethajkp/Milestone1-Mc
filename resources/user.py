import random
import sqlite3


#import data as data

from flask_jwt import jwt_required
from flask_mail import Message, Mail
from flask_restful import Resource, reqparse

#from app import app
from models.user import UserModel

from datetime import date
from random import randint
from urllib.parse import quote
import webbrowser

today = date.today()


class UserRegister(Resource):
    TABLE_NAME = 'user'

    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('date_of_birth',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('contact_no',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('qualification',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('gender',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('salary',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pan_no',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type_of_employer',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('name_of_employer',
                        type=str,
                        required=True,

                        )

    @jwt_required()
    def get(self, email):
        user = UserModel.find_by_email(email)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    @jwt_required()
    def get(self, user_id):
        user = UserModel.find_by_user_id(user_id)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    @jwt_required()
    def get(self, user_id, password):
        user = UserModel.find_by_login(user_id, password)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    @jwt_required()
    def get(self, password):
        user = UserModel.find_by_password(password)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404



    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {"message": "User with that email id already exists."}, 400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        income = int(data['salary'])
        salary_per_year = income*12
        print(f"{salary_per_year}")
        print(type(salary_per_year))
        if int(salary_per_year) <= 500000:
            user_type_id = 'A'
        elif int(salary_per_year) > 500000 & int(salary_per_year) <= 1000000:
            user_type_id = 'B'
        elif int(salary_per_year) > 1000000 & int(salary_per_year) <= 1500000:
            user_type_id = 'C'
        elif int(salary_per_year) > 1500000 & int(salary_per_year) <= 3000000:
            user_type_id = 'D'
        elif int(salary_per_year) > 3000000:
            user_type_id = 'E'
        print(user_type_id)


        num = randint(1_200, 9999)

        print(num)
        user_id = user_type_id + '-' + str(num)
        date = today.strftime("%d")

        month = today.strftime("%B")

        random_number = randint(100, 999)
        character = random.choice('$_')
        password = str(date) + str(month) + str(character) + str(random_number)
        #msg = Message('Dear User,', sender='madhupreetha98@gmail.com', recipients=[data['email']])
        #msg.body = "Your user id is " + data['user_id'] + " and your password is " + data['password']
        query = "INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)".format(
            table=self.TABLE_NAME)
        cursor.execute(query, (data['first_name'], data['last_name'], data['date_of_birth'], data['address'], data['contact_no'], data['email'], data['qualification'], data['gender'], data['salary'], data['pan_no'],
                       data['type_of_employer']
                       , data['name_of_employer'], user_id, password))
        connection.commit()


        connection.close()

       # mail.send(msg)

        return {"message": "User created successfully."}, 201





class UserList(Resource):
      def get(self):
           return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
