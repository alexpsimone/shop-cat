"""Models for Shop Cat app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


class Procedure(db.Model):
    """A procedure."""

    __tablename__ = 'procedures'

    proc_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True)
    title = db.Column(db.String(25), nullable = False, unique = True)
    description = db.Column(db.Text, default = '')
    label = db.Column(db.String(25), default = '')
    img = db.Column(db.String, default = '')
    page_id = db.Column(db.Integer, db.ForeignKey('pages.page_id'))
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    page = db.relationship('Page', backref = 'procedures')
    user = db.relationship('User', backref = 'procedures')

    def __repr__(self):
        return f'<Procedure proc_id={self.proc_id} title={self.title}>'


class Page(db.Model):
    """A page."""

    __tablename__ = 'pages'

    page_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True)
    size = db.Column(db.Float, default=0)
    page_url = db.Column(db.String(50), unique = True)
    page_type = db.Column(db.String(25))

    def __repr__(self):
        return f'<Page page_id={self.page_id} page_url={self.page_url}>'





def connect_to_db(flask_app, db_uri='postgresql:///shopcat', echo = True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    print('Connected to Shop Cat database!')


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
