"""Models for Shop Cat app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    nickname = db.Column(db.String(25))
    avatar_img_url = db.Column(db.String, default="cat.jpg")

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"


class Procedure(db.Model):
    """A procedure."""

    __tablename__ = "procedures"

    proc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50), default="")
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="procedures")

    def __repr__(self):
        return f"<Procedure proc_id={self.proc_id} title={self.title}>"


class Step(db.Model):
    """A Step in a procedure."""

    __tablename__ = "steps"

    step_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_num = db.Column(db.Integer, default=0)
    reference = db.Column(db.String, default="No Ref Provided")
    step_text = db.Column(db.Text, nullable=False)
    step_img = db.Column(db.String, default="/static/img/toolbox.png")
    proc_id = db.Column(db.Integer, db.ForeignKey("procedures.proc_id"))
    
    proc = db.relationship("Procedure", backref="steps")

    def __repr__(self):
        return f"""<Step step_id={self.step_id} proc={self.proc} 
                        order_num={self.order_num}>"""


class Car(db.Model):
    """A car."""

    __tablename__ = "cars"

    car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(125), nullable=False)
    make = db.Column(db.String(125), default="unknown")
    model_year = db.Column(db.Integer, default=9999)

    def __repr__(self):
        return f"""<Car car_id={self.car_id} 
                    model_year={self.model_year} model={self.model}>"""


class Tool(db.Model):
    """A tool."""

    __tablename__ = "tools"

    tool_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    tool_img = db.Column(db.String)

    def __repr__(self):
        return f"<Tool tool_id={self.tool_id} name={self.name}>"


class PartNum(db.Model):
    """A part number."""

    __tablename__ = "part_nums"

    part_num_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manuf = db.Column(db.String(25), default="unknown")
    part_num = db.Column(db.String(25), default="unknown")
    is_oem_part = db.Column(db.Boolean)
    part_id = db.Column(db.Integer, db.ForeignKey("parts.part_id"))

    part = db.relationship("Part", backref="part_nums")

    def __repr__(self):
        return f"""<PartNum part_num_id={self.part_num_id} 
                    part_num={self.part_num}>"""


class Part(db.Model):
    """A part."""

    __tablename__ = "parts"

    part_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    part_img = db.Column(db.String(50))

    def __repr__(self):
        return f"<Part part_id={self.part_id} name={self.name}>"


class ProcedureCar(db.Model):
    """Procedure-Car association table."""

    __tablename__ = "procedure_cars"

    proc_car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proc_id = db.Column(db.Integer, db.ForeignKey("procedures.proc_id"))
    car_id = db.Column(db.Integer, db.ForeignKey("cars.car_id"))

    proc = db.relationship("Procedure", backref="procedure_car")
    car = db.relationship("Car", backref="procedure_car")

    def __repr__(self):
        return f"""<ProcedureCar proc_car_id={self.proc_car_id} 
                    procedure={self.proc_id} car={self.car_id}>"""


class ProcedurePart(db.Model):
    """Procedure-Part association table."""

    __tablename__ = "procedure_parts"

    proc_part_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proc_id = db.Column(db.Integer, db.ForeignKey("procedures.proc_id"))
    part_id = db.Column(db.Integer, db.ForeignKey("parts.part_id"))

    proc = db.relationship("Procedure", backref="procedure_part")
    part = db.relationship("Part", backref="procedure_part")

    def __repr__(self):
        return f"""<ProcedurePart proc_part_id={self.proc_part_id} 
                    procedure={self.proc_id} part={self.part_id}>"""


class ProcedureTool(db.Model):
    """Procedure-Tool association table."""

    __tablename__ = "procedure_tools"

    proc_tool_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proc_id = db.Column(db.Integer, db.ForeignKey("procedures.proc_id"))
    tool_id = db.Column(db.Integer, db.ForeignKey("tools.tool_id"))

    proc = db.relationship("Procedure", backref="procedure_tool")
    tool = db.relationship("Tool", backref="procedure_tool")

    def __repr__(self):
        return f"""<ProcedureTool proc_tool_id={self.proc_tool_id} 
                    procedure={self.proc_id} tool={self.tool_id}>"""


def connect_to_db(flask_app, db_uri="postgresql:///shopcat", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to Shop Cat database!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
