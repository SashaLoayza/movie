from db import db, User, Movie, Event
from flask import Flask, request
import json
from datetime import datetime
from webscrape import event_tuples_sp22

app = Flask(__name__)

db_filename = "movie.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

# -- initializes app ----------
db.init_app(app)
with app.app_context():
    db.create_all()
    for event in event_tuples_sp22:
        new_event = Event(name=event[0],location='Willard Straight Hall',start=event[1],end=event[2],host='Cornell Cinema')
        db.session.add(new_event)
        db.session.commit()
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
    return success_response({"users": [u.serialize() for u in User.query.all()] })

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
    name = body.get("name")
    password = body.get("password")
    if username is None or password is None or name is None:
        return failure_response("Username, name, or password wasn't provided", 400)
    new_user = User(username=username, name = name, pasword=password)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/username/", methods=["POST"])
def edit_username(user_id):
    """
    Edits a users username
    """
    body = json.loads(request.data)
    return _edit_user_value(body.get("username"), user_id, True)

@app.route("/api/users/<int:user_id>/password/", methods=["POST"])
def edit_password(user_id):
    """
    Edits a users password
    """
    body = json.loads(request.data)
    return _edit_user_value(body.get("password"), user_id, False)


@app.route("/api/users/<int:user_id>/add_movie/", methods=["POST"])
def add_movie_to_user(user_id):
    """
    Adds a watched or interested movie to a user (depending on body request)
    """
    body = json.loads(request.data)
    movie_id = body.get("movie_id")
    movie_type = body.get("movie_type")
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        return failure_response("Movie not found")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    if movie_type == "watched":
        user.movies_watched.append(movie)
    elif movie_type == "interested":
        user.movies_interested.append(movie)
    else:
        return failure_response("Invalid request body")
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/add_event/", methods=["POST"])
def add_event_to_user(user_id):
    """
    Adds a hosted or interested event to a user (depending on body request)
    """
    body = json.loads(request.data)
    event_id = body.get("event_id")
    event_type = body.get("event_type")
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return failure_response("Event not found")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    if event_type == "host":
        user.events_hosted.append(event)
    elif event_type == "interested":
        user.events_interested.append(event)
    else:
        return failure_response("Invalid request body")
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

# -- helper methods for User routes --

def _edit_user_value(value_to_change, user_id, is_username):
    """
    Helper method to change a value in user associated with user_id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    if is_username:
        user.username = value_to_change 
    else:
        user.password = value_to_change
    db.session.commit() 
    return success_response(user.serialize(), 201)

# -- movie routes ----------
@app.route("/api/movies/")
def get_all_movies():
    """
    Gets all movies
    """
    return success_response({"movies": [m.serialize() for m in Movie.query.all()] })

@app.route("/api/movies/<int:movie_id>/")
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
    body = json.loads(request.data)
    name = body.get("name")
    rating = body.get("rating")
    description = body.get("description")
    if name is None or not valid_rating(rating) or description is None:
        return failure_response("Invlaid request body")
    new_movie = Movie(name=name, rating=rating, description=description)
    db.session.add(new_movie)
    db.session.commit()
    return success_response(new_movie.serialize(), 201)

@app.route("/api/movies/<int:movie_id>/rating/", methods=["POST"])
def edit_movie_rating(movie_id):
    """
    Edits a movies rating
    """
    body = json.loads(request.data)
    rating = body.get("rating")
    if rating is None:
        return failure_response("Invalid request body")
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        return failure_response("Movie not found")
    movie.rating = rating
    db.session.commit()
    return success_response(movie.serialize(), 201)

@app.route("/api/movies/<int:movie_id>/description/", methods=["POST"])
def edit_movie_description(movie_id):
    """
    Edits a movies description
    """
    body = json.loads(request.data)
    description = body.get("description")
    if description is None:
        return failure_response("Invalid request body")
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        return failure_response("Movie not found")
    movie.description = description
    db.session.commit()
    return success_response(movie.serialize(), 201)

@app.route("/api/movies/<int:movie_id>/", methods=["DELETE"])
def delete_movie(movie_id):
    """
    Deletes a movie
    """
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        return failure_response("Movie not found")
    db.session.delete(movie)
    db.session.commit()
    return success_response(movie.serialize())

# -- helper methods for movie routes --

def valid_rating(rating):
    """
    Returns False if rating is number between 0 and 5, else False.
    """
    if isinstance(rating,(int, float)):
        if 0 <= rating <= 5:
            return True
    return False
    
    
# -- event routes ----------
@app.route("/api/events/", methods=["GET"])
def get_all_events():
    """
    Gets all events
    """
    return success_response({"events": [e.serialize() for e in Event.query.all()] })

@app.route("/api/events/<int:event_id>/")
def get_specific_event(event_id):
    """
    Get a specific event by id
    """
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return failure_response("Event not found")
    return success_response(event.serialize())


@app.route("/api/events/", methods=["POST"])
def create_event():
    """
    Create a new event
    """
    body = json.loads(request.data)
    name = body.get("name")
    location = body.get("location")
    start = datetime(2012, 10, 10, 10, 10, 10)
    end = datetime(2012, 11, 10, 11, 11, 11)
    if name is None is location is None or start is None or end is None:
        return failure_response("Invalid request body")
    event = Event(name=name, location=location, start=start, end=end)
    db.session.add(event)
    db.session.commit()
    return success_response(event.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
