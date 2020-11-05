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


class Car(db.Model):
    """A car."""

    __tablename__ = 'cars'

    car_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True)
    model = db.Column(String(25), nullable = False)
    make = db.Column(String(25), default = 'unknown')
    model_year = db.Column(Integer, default = 9999)

    def __repr__(self):
        return f'<Car car_id={self.car_id} model_year={self.model_year} model={self.model}>'


class Tool(db.Model):
    """A tool."""

    __tablename__ = 'tools'

    tool_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True)
    name = db.Column(String(25), nullable = False)
    description = db.Column(Text)
    tool_img = db.Column(db.String, default = '')

    def __repr__(self):
        return f'<Tool tool_id={self.tool_id} name={self.name}>'


class PartNum(db.Model):
    """A part number."""

    __tablename__ = 'part_nums'

    part_num_id = db.Column(db.Integer,
                            primary_key = True,
                            autoincrement = True)
    manuf = db.Column(String(25), default='unknown')
    part_num = db.Column(String(25), default='unknown')
    is_oem_part = db.Column(Bool)

    def __repr__(self):
        return f'<PartNum part_num_id={self.part_num_id} part_num={self.part_num}>'


class Part(db.Model):
    """A part."""

    __tablename__ = 'parts'

    part_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True)
    name = db.Column(String(25), nullable = False)
    part_img = db.Columndb.Column(db.String(50))
    part_num_id = db.Column(db.Integer, db.ForeignKey('part_nums.part_num_id'))

    part_number = db.relationship('PartNum', backref = 'parts')

    def __repr__(self):
        return f'<Part part_id={self.part_id} name={self.name}>'


class ProcedureCar(db.Model):
    """Procedure-Car association table."""

    __tablename__ = 'procedure_car'

    proc_car_id = db.Column(db.Integer,
                            primary_key = True,
                            autoincrement = True)
    proc_id = db.Column(db.Integer, db.ForeignKey('procedures.proc_id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'))

    proc = db.relationship('Procedure', backref = 'procedure_car')
    car = db.relationship('Car', backref = 'procedure_car')

    def __repr__(self):
        return f'<ProcedureCar proc_car_id={self.proc_car_id} procedure={self.proc_id} car={self.car_id}>'


class ProcedurePart(db.Model):
    """Procedure-Part association table."""

    __tablename__ = 'proc_part'

    proc_part_id = db.Column(db.Integer,
                            primary_key = True,
                            autoincrement = True)
    proc_id = db.Column(db.Integer, db.ForeignKey('procedures.proc_id'))
    part_id = db.Column(db.Integer, db.ForeignKey('parts.part_id'))

    proc = db.relationship('Procedure', backref = 'procedure_car')
    car = db.relationship('Part', backref = 'procedure_car')

    def __repr__(self):
        return f'<ProcedureCar proc_car_id={self.proc_car_id} procedure={self.proc_id} part={self.part_id}>'


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
