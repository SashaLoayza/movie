from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table(
    "association",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"))
)

interested_table = db.Table(
    "interested_table",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"))
)

events_interested_table = db.Table(
    "events_interested_table",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("events.id"))
)


class Users(db.Model):
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
        "Movies", secondary=association_table, back_populates="users_watched")
    movies_hosted = db.relationship(
        "Events", back_populates="host", cascade="delete")
    interested = db.relationship(
        "Movies", secondary=interested_table,
        back_populates="users_interested")
    events_interested = db.relationship(
        "Events", secondary=events_interested_table,
        back_populates="users_interested")

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
            "movies_watched": [m.serialize() for m in self.movies_watched]
        }


class Movies(db.Model):
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
        'Users', secondary=association_table, back_populates="movies_watched")
    users_interested = db.relationship(
        'Users', secondary=interested_table, back_populates="interested")

# Events Models


class Events(db.Model):
    """
    A class to model all events-
    Cornell Cinema movies as well as Community movies.
    Has a many to one relationship with Users (movie -> host)
    Has a many-to-many relationship with Users (movie -> users_interested)
    """
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"))
    host = db.relationship(
        "Users", back_populates="movies_hosted", cascade="delete")
    users_interested = db.relationship(
        'Users', secondary=events_interested_table, back_populates="events_interested")
