"""Models for Shop Cat app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Procedure(db.Model):
    """A procedure."""

    __tablename__ = 'procedures'

    proc_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True)
    title = db.Column(db.String(25), nullable = False, unique = True)
    description = db.Column(db.Text)
    label = db.Column(db.String(25))
    img = db.Column(db.String)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.page_id'))
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    page = db.relationship('Page')
    user = db.relationship('User')

    def __repr__(self):
        return f'<Procedure proc_id={self.proc_id} title={self.title}>'


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
