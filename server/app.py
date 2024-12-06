#!/usr/bin/env python3

from flask import request, session, make_response, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from config import app, db, api
from models import User, Recipe
from werkzeug.exceptions import UnprocessableEntity, Unauthorized


bcrypt = Bcrypt(app)

class Signup(Resource):
    def post(self):
            data = request.get_json()
            if 'username' not in data:
                raise UnprocessableEntity(description="Username is required")
            print(data)
            new_user = User(
                username = data['username'],
                image_url = data['image_url'],
                bio = data['bio']
            )
            new_user.password_hash = data['password']
            print(new_user.to_dict())
            db.session.add(new_user)
            db.session.commit()
            response = make_response(new_user.to_dict(), 201)
            return response
        
@app.errorhandler(UnprocessableEntity)
def handle_bad_request_error(e):
    return jsonify(error=str(e)), 422

class CheckSession(Resource):
    def get(self):
        if session['user_id']:
            id = session['user_id']
            print("SESSION ID!", id)
            user = User.query.filter_by(id=id).first().to_dict()
            print('EAT THIS', user)
            user_no_pass = {
                'id': session['user_id'],
                'username': user['username'],
                'image_url': user['image_url'],
                'bio': user['bio']
            }
            response = make_response(user_no_pass, 200)
            return response
        else:
            response = make_response("Not authorized", 401)
            return response
        pass

class Login(Resource):
    def post(self):
        user_object = request.get_json()
        user = User.query.filter(User.username == user_object['username']).first()
        if user:
            if user.authenticate(user_object['password']):
                session['user_id'] = user.id
                return user.to_dict(), 200
        else:
            raise Unauthorized("Username or password are incorrect")
    
@app.errorhandler(Unauthorized)
def handle_bad_request_error(e):
    return jsonify(error=str(e)), 401


class Logout(Resource):
    def delete(self):
        if session["user_id"]:
            session["user_id"] = None
            return {}, 204
        else:
            raise Unauthorized("You are not logged in")

class RecipeIndex(Resource):
    def get(self):
        if session["user_id"]:
            user = User.query.filter_by(id = session["user_id"]).first()
            recipe_list = [recipe.to_dict() for recipe in user.recipes]
            print(recipe_list)
            response = make_response(recipe_list, 200)
            return response
        else:
            raise Unauthorized("You are not logged in") 
    
    def post(self):
        if session["user_id"]:
            recipe = request.get_json()
            required_attributes = ['title', 'instructions', 'minutes_to_complete']
            missing_attributes = [attr for attr in required_attributes if attr not in recipe or not recipe[attr]]
            
            if missing_attributes:
                raise UnprocessableEntity(description=f"The recipe is missing required attributes: {', '.join(missing_attributes)}")

            if len(recipe['instructions']) < 50:
                raise UnprocessableEntity(description=f"The recipe is missing required attributes: {', '.join(missing_attributes)}")
            response_object = Recipe(
                title=recipe['title'],
                instructions=recipe['instructions'],
                minutes_to_complete=recipe['minutes_to_complete']
            )

            user = User.query.filter_by(id=session["user_id"]).first()
            if not user:
                raise UnprocessableEntity(description="User not found")

            response_object.user = user

            db.session.add(response_object)
            db.session.commit()

            response = make_response(response_object.to_dict(), 201)
            return response
        else:
            raise Unauthorized("You are not logged in")

class Clear(Resource):
    def get(self):
        session['user_id'] = None
        return {}, 204
api.add_resource(Clear, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)