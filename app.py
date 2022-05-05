from db import db, User, Movie, Event
from flask import Flask, request
import json

app = Flask(__name__)

db_filename = "movie.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

# -- initializes app ----------
db.init_app(app)
with app.app_context():
    db.create_all()

# -- generalized responses ----------
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# -- users routes ----------
@app.route("/api/users/")
def get_all_users():
    """
    Gets all users
    """
    return success_response({"users": [u.serialize() for u in Users.query.all()] })

@app.route("/api/users/<int:user_id>/")
def get_specific_user(user_id):
    """
    Gets a user by its user_id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Creates a new user
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    if username is None or password is None:
        return failure_response("Username or password wasn't provided", 400)
    new_user = User(username=username, pasword=password)
    db.session.add(new_user)
    db.session.commit()
    serialized_user = new_user.serialize()
    serialized_user["movies_watched"] = []
    serialized_user["movies_interested"] = []
    serialized_user["movies_hosted"] = []
    serialized_user["movies_interested"] = []
    return success_response(serialized_user, 201)

@app.route("/api/users/<int:user_id>/", methods=["POST"])
def edit_username(user_id):
    """
    Edits a users username
    """
    body = json.loads(request.data)
    new_username = body.get("username")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    user.username = new_username 
    db.session.commit() 
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Deletes a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

# -- movie routes ----------
@app.route("/api/movies/<int:movie_id>/", methods=["POST"])
def get_specific_movie(movie_id):
    """
    Get a movie by its id
    """
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        return failure_response("Movie not found")
    return success_response(movie.serialize())

@app.route("/api/movies/", methods=["POST"])
def create_movie():
    """
    Creates a new movie 
    """

#get all movies

#get all events

    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
