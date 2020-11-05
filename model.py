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
