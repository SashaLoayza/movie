from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

watched_table = db.Table(
    "watched_table",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"))
)

interested_table = db.Table(
    "interested_table",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"))
)

events_hosted_table = db.Table(
    "events_hosted_table",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("events.id"))
)

events_interested_table = db.Table(
    "events_interested_table",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("events.id"))
)


class User(db.Model):
    """
    A class to model the users database for the movie app
    Has a many to many relationship with Movies (movies watched)
    Has a one to many relationship with Events (movies hosted)
    Has a many to many relationship with Events (movies interested in)
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    movies_watched = db.relationship(
        "Movie", secondary=watched_table, back_populates="users_watched", cascade="delete")
    movies_interested = db.relationship(
        "Movie", secondary=interested_table, back_populates="users_interested", cascade="delete")

    events_hosted = db.relationship(
        "Event", secondary=events_hosted_table, back_populates="host", cascade="delete")
    events_interested = db.relationship(
        "Event", secondary=events_interested_table, back_populates="users_interested", cascade="delete")

    def __init__(self, **kwargs):
        """
        Method to initialize a new user database entry
        """
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")

    def serialize(self):
        """
        Return a serialized representation of a user database entry
        """
        return {
            "id": self.id,
            "username": self.username,
            "movies_watched": [m.serialize() for m in self.movies_watched],
            "movies_interested": [m.serialize() for m in self.movies_interested],
            "events_hosted": [e.serialize() for e in self.events_hosted],
            "events_interested": [e.serialize() for e in self.events_interested]
        }


class Movie(db.Model):
    """
    A class to model the movies database for the movie app
    Has a many-to-many relationship with Users (movie -> users_watched)
    Has a many-to-many relationship with Users (movie -> users_interested)
    """
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    description = db.Column(db.String, nullable=False)
    users_watched = db.relationship(
        'User', secondary=watched_table, back_populates="movies_watched")
    users_interested = db.relationship(
        'User', secondary=interested_table, back_populates="movies_interested")

    def __init__(self, **kwargs):
        """
        Method to initialize a new movie database entry
        """
        self.name = kwargs.get("name", "")
        self.rating = kwargs.get("rating", 0)
        self.description = kwargs.get("description", "")

    def serialize(self):
        """
        Return a serialized representation of a movie database entry
        """
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "description": self.description
        }


class Event(db.Model):
    """
    A class to model all events-
    Cornell Cinema movies as well as Community movies.
    Has a many to one relationship with Users (movie -> host)
    Has a many-to-many relationship with Users (movie -> users_interested)
    """
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.DateTime, nullable=False)
    host = db.relationship(
        "User", secondary = events_hosted_table, back_populates="events_hosted", cascade="delete")
    users_interested = db.relationship(
        'User', secondary=events_interested_table, back_populates="events_interested", cascade="delete")

    def __init__(self, **kwargs):
        """
        Method to initialize a new event database entry
        """
        self.name = kwargs.get("name", "")
        self.location = kwargs.get("location", "")
        self.start = kwargs.get("start")
        self.duration = kwargs.get("duration")

    def serialize(self):
        """
        Returns a serialized version of the event database entry
        """
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start": self.start,
            "duration": self.duration
        }
