from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table(
    "assocation",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"))
)

class Users(db.Model):
    """
    A class to model the users database for the movie app
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    movies_watched = db.relationship("Movies", cascade='delete')
    users = db.relationship("Users", secondary=association_table, back_populates="users")

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
    """
    __tablename__ = "movies"