"""Models for Shop Cat app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Page(db.Model):
    """A page."""

    __tablename__ = 'pages'

    page_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True)
    size = db.Column(db.Real)
    page_url = db.Column(db.String(50), unique = True)
    page_type = db.Column(db.String(25))

    def __repr__(self):
        return f'<Page page_id={self.page_id} page_url={self.page_url}>'


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    password = db.Column(db.String(25), nullable = False)
    nickname = db.Column(db.String(25))
    avatar_img_url = db.Column(db.String) 

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'
