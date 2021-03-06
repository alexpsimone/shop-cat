from flask import Flask, render_template, redirect, send_from_directory
from flask import request, flash, session, jsonify
from jinja2 import StrictUndefined
from werkzeug.utils import secure_filename
import requests, json
import os
from random import shuffle

from model import db, connect_to_db, User, Procedure, Car, Part, Tool, Step
from model import PartNum, ProcedureCar, ProcedurePart, ProcedureTool
import crud

app = Flask(__name__)

UPLOAD_FOLDER = "static/img/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_login():
    """Render the landing/login page."""

    if session:
        return redirect("/home")
    else:
        return render_template("shopcat.html")


############################################################
#### TODO: Maybe integrate request.json to make smaller? ###
############################################################
@app.route("/build-procedure", methods=["POST"])
def build_procedure():
    """Build a procedure with the info given in the form."""

    # Take the form data to create a Procedure object.
    proc_title = request.form.get("proc_title")
    proc_label = request.form.get("proc_label")

    user = User.query.filter_by(user_id=session["current_user"]).first()

    procedure = Procedure(title=proc_title, label=proc_label, user=user)
    db.session.add(procedure)

    # For each step added by the user, create a Step object.
    NUM_STEPS = int(request.form.get("NUM_STEPS"))

    for step in range(1, (NUM_STEPS + 1)):

        step_text = request.form.get(f"step_text_{step}")
        ref_text = request.form.get(f"ref_text_{step}")
        step_img = request.files[f"step_img_{step}"]

        reference = crud.get_step_ref(ref_text)
        filename = crud.get_step_img(step_img)

        new_step = Step(
            order_num=step,
            step_text=step_text,
            proc=procedure,
            reference=reference,
            step_img=filename,
        )
        db.session.add(new_step)

    """
    Check if the user selected an existing car.
    If they did, then keep it handy, and don't create a new Car object.
    If they didn't, then use the session info to create one.
    """
    model_year = session["model_year"]
    make = session["make"]
    model = session["model"]

    if Car.query.filter_by(model_year=model_year, make=make, model=model).first():
        car = Car.query.filter_by(model_year=model_year, make=make, model=model).first()
    else:
        car = Car(model=model, make=make, model_year=model_year)
        db.session.add(car)

    # Use the Car and Procedure objects to make a new ProcedureCar.
    proc_car = ProcedureCar(proc=procedure, car=car)
    db.session.add(proc_car)
    db.session.flush()

    # Retrieve procedure ID after 1st commit, to render procedure page later
    proc_id = procedure.proc_id

    # Add tools to the procedure based on form info.
    NUM_TOOLS = int(request.form.get("NUM_TOOLS"))

    for tool in range(1, (NUM_TOOLS + 1)):

        tool_req = request.form.get(f"tool_req_{tool}")
        tool_other = request.form.get(f"tool_other_{tool}")
        tool_img = request.files[f"tool_img_{tool}"]

        my_tool = crud.create_tool(tool_req, tool_other, tool_img)

        proc_tool = ProcedureTool(proc=procedure, tool=my_tool)
        db.session.add(proc_tool)
        db.session.flush()

    # Add parts to the procedure based on form info.
    NUM_PARTS = int(request.form.get("NUM_PARTS"))

    for part in range(1, (NUM_PARTS + 1)):

        part_req = request.form.get(f"part_req_{part}")
        part_img = request.files[f"part_img_{part}"]
        part_other = request.form.get(f"part_{part}_other_name")
        part_other_num = request.form.get(f"part_{part}_other_num")
        part_other_manuf = request.form.get(f"part_{part}_other_manuf")
        oem = request.form.get(f"oem_{part}") == "True"

        my_part = crud.create_part(
            part_req, part_other, part_img, part_other_num, part_other_manuf, oem
        )

        proc_part = ProcedurePart(proc=procedure, part=my_part)
        db.session.add(proc_part)
        db.session.flush()

    db.session.commit()

    return redirect(f"procedure/{proc_id}")


@app.route("/dashboard/<user_id>")
def show_dashboard(user_id):
    """Render the user dashboard."""

    if session:

        user = User.query.filter_by(user_id=user_id).first()
        procedures = Procedure.query.filter_by(created_by_user_id=user_id).all()
        model_year = session.get("model_year")
        make = session.get("make")
        model = session.get("model")

        return render_template(
            "dashboard.html",
            user=user,
            procedures=procedures,
            model_year=model_year,
            make=make,
            model=model,
        )
    else:
        return redirect("/")


@app.route("/edit-procedure/<proc_id>")
def edit_procedure(proc_id):
    """Render the procedure editing form."""

    if session:
        user = User.query.filter_by(user_id=session["current_user"]).first()
        procedure = Procedure.query.get(proc_id)
        proc_car_obj = ProcedureCar.query.filter_by(proc_id=proc_id).all()
        proc_part_obj = ProcedurePart.query.filter_by(proc_id=proc_id).all()
        proc_tool_obj = ProcedureTool.query.filter_by(proc_id=proc_id).all()
        num_tools = ProcedureTool.query.filter_by(proc_id=proc_id).count()
        num_parts = ProcedurePart.query.filter_by(proc_id=proc_id).count()
        num_cars = ProcedureCar.query.filter_by(proc_id=proc_id).count()
        num_steps = Step.query.filter_by(proc_id=proc_id).count()
        steps = Step.query.filter_by(proc_id=proc_id).all()
        sorted_makes = crud.get_all_rockauto_makes()

        return render_template(
            "edit-procedure.html",
            user=user,
            procedure=procedure,
            proc_car_obj=proc_car_obj,
            proc_part_obj=proc_part_obj,
            proc_tool_obj=proc_tool_obj,
            steps=steps,
            num_tools=num_tools,
            num_parts=num_parts,
            num_cars=num_cars,
            num_steps=num_steps,
            sorted_makes=sorted_makes,
        )
    else:
        return redirect("/")

    return render_template("edit-procedure.html")


@app.route("/existing-user", methods=["POST"])
def login_user():
    """Log in with an existing user account."""

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user:
        if user.password == password:
            session["current_user"] = user.user_id
            return redirect("/home")
        else:
            flash("Password is incorrect.")
            return redirect("/login")
    else:
        flash(f"No account exists with this username")
        return redirect("/login")


@app.route("/get-model-years.json")
def get_all_model_years():

    make = request.args.get("make")
    model_years = crud.get_all_rockauto_model_years(make)

    return jsonify(model_years)


@app.route("/get-models.json")
def get_all_models():

    make = request.args.get("make")
    model_year = request.args.get("modelYear")
    models = crud.get_all_rockauto_models(make, model_year)

    return jsonify(models)

    ####################################
    ##### Using NHTSA Vehicle API: #####
    ####################################
    # all_models = []
    # url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeYear/make/{make}/modelyear/{model_year}?format=json"
    # res = requests.get(url)
    # data = res.json()

    # for item in data["Results"]:
    #     all_models.append(item["Model_Name"])
    # sorted_models = sorted(all_models)

    # return jsonify(sorted_models)


@app.route("/get-parts.json")
def get_all_parts():
    """Get all parts from the shopcat database and return as JSON."""

    parts = [part.name for part in Part.query.all()]

    return jsonify(parts)


@app.route("/get-tools.json")
def get_all_tools():
    """Get all tools from the shopcat database and return as JSON."""

    tools = [tool.name for tool in Tool.query.all()]

    return jsonify(tools)


@app.route("/home")
def show_homepage():
    """Render the homepage."""

    if session:
        user = User.query.filter_by(user_id=session["current_user"]).first()
        proc_car_objs = ProcedureCar.query.all()
        shuffle(proc_car_objs)
        featured = proc_car_objs[:12]

        tools = Tool.query.all()
        cars = Car.query.all()
        makes = sorted(set([car.make for car in cars]))

        return render_template(
            "homepage.html",
            user=user,
            proc_car_objs=featured,
            tools=tools,
            makes=makes,
        )
    else:
        return redirect("/")


@app.route("/login")
def login_page():
    """Render the login page."""

    return render_template("login.html")


@app.route("/new-user", methods=["POST"])
def new_user():
    """Create a new user."""

    username = request.form.get("username")
    password = request.form.get("password")
    nickname = request.form.get("nickname")

    user = User.query.filter_by(username=username).first()

    if user:
        flash("A user already exists with that username.")
        return redirect("/")
    else:
        user = User(username=username, password=password, nickname=nickname)
        db.session.add(user)
        db.session.commit()
        flash(f"New account created. Please use your credentials to log in.")
        return redirect("/login")


@app.route("/part/<part_id>")
def show_part_page(part_id):
    """Render a part page."""

    user = User.query.filter_by(user_id=session["current_user"]).first()
    part = Part.query.filter_by(part_id=part_id).first()
    proc_parts = set(ProcedurePart.query.filter_by(part=part).all())

    all_cars = set()

    for proc_part in proc_parts:
        proc = proc_part.proc
        proc_cars = set(ProcedureCar.query.filter_by(proc=proc).all())
        for proc_car in proc_cars:
            all_cars.add(proc_car.car)

    part_nums = PartNum.query.filter_by(part=part).all()
    print("*********************************", part_nums)

    return render_template(
        "part.html",
        part=part,
        user=user,
        proc_parts=proc_parts,
        all_cars=all_cars,
        part_nums=part_nums,
    )


@app.route("/procedure/<proc_id>")
def show_procedure_page(proc_id):
    """Render a procedure page."""

    if session:
        user = User.query.filter_by(user_id=session["current_user"]).first()
        procedure = Procedure.query.get(proc_id)
        proc_car_obj = ProcedureCar.query.filter_by(proc_id=proc_id).all()
        proc_part_obj = ProcedurePart.query.filter_by(proc_id=proc_id).all()
        proc_tool_obj = ProcedureTool.query.filter_by(proc_id=proc_id).all()
        steps = Step.query.filter_by(proc_id=proc_id).order_by(Step.order_num).all()
        proc_num_tools = ProcedureTool.query.filter_by(proc_id=proc_id).count()
        proc_num_parts = ProcedurePart.query.filter_by(proc_id=proc_id).count()
        proc_num_steps = Step.query.filter_by(proc_id=proc_id).count()

        return render_template(
            "procedure.html",
            user=user,
            procedure=procedure,
            proc_car_obj=proc_car_obj,
            proc_part_obj=proc_part_obj,
            proc_tool_obj=proc_tool_obj,
            steps=steps,
            proc_num_tools=proc_num_tools,
            proc_num_parts=proc_num_parts,
            proc_num_steps=proc_num_steps,
        )
    else:
        return redirect("/")


@app.route("/rebuild-procedure", methods=["POST"])
def rebuild_procedure():
    """Rebuild an edited procedure."""

    # Retrieve the procedure to be edited.
    proc_id = int(request.form.get("proc_id"))

    # Retrieve the procedure title.
    title = request.form.get("title")

    # Retrieve the label.
    label = request.form.get("proc_label")

    # Retrieve all cars listed on the form.
    cars = request.form.getlist("cars")

    # Iterate through all tools on the form. Make  a list of tuples (?)
    # containing this information.
    NUM_TOOLS = int(request.form.get("NUM_TOOLS"))

    tool_data = {}

    for tool in range(1, (NUM_TOOLS + 1)):

        tool_id = request.form.get(f"tool-id-{tool}")
        tool_name = request.form.get(f"tool-name-{tool}")
        tool_existing_img = request.form.get(f"tool-existing-img-{tool}")
        tool_img = request.files[f"tool-img-{tool}"]
        tool_other = request.form.get(f"tool-other-name-{tool}")

        if tool_img != None and crud.allowed_file(tool_img.filename):
            filename = secure_filename(tool_img.filename)
            tool_img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            tool_img.close()
        elif tool_existing_img:
            filename = tool_existing_img
        else:
            filename = "toolbox.png"

        tool_data[tool] = {}
        tool_data[tool]["id"] = tool_id
        tool_data[tool]["name"] = tool_name
        tool_data[tool]["img"] = filename
        tool_data[tool]["other"] = tool_other

    # Iterate through all parts on the form. Make  a list of tuples (?)
    # containing this information.
    NUM_PARTS = int(request.form.get("NUM_PARTS"))

    part_data = {}

    for part in range(1, (NUM_PARTS + 1)):

        part_id = request.form.get(f"part-id-{part}")
        part_name = request.form.get(f"part-name-{part}")
        part_existing_img = request.form.get(f"part-existing-img-{part}")
        part_img = request.files[f"part-img-{part}"]
        part_other = request.form.get(f"part-other-name-{part}")
        part_pn = request.form.get(f"part-other-pn-{part}")
        part_manuf = request.form.get(f"part-other-manuf-{part}")
        part_oem = request.form.get(f"part-other-oem-{part}") == "True"

        if part_img != None and crud.allowed_file(part_img.filename):
            filename = secure_filename(part_img.filename)
            part_img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            part_img.close()
        elif part_existing_img:
            filename = part_existing_img
        else:
            filename = "toolbox.png"

        part_data[part] = {}
        part_data[part]["id"] = part_id
        part_data[part]["name"] = part_name
        part_data[part]["img"] = filename
        part_data[part]["other"] = part_other
        part_data[part]["pn"] = part_pn
        part_data[part]["manuf"] = part_manuf
        part_data[part]["oem"] = part_oem

    # Iterate through all steps on the form. Make  a list of tuples (?)
    # containing this information.
    step_data = {}
    NUM_STEPS = int(request.form.get("NUM_STEPS"))

    for step in range(1, (NUM_STEPS + 1)):

        step_id = request.form.get(f"step-id-{step}")
        step_order = request.form.get(f"step-order-{step}")
        step_text = request.form.get(f"step-text-{step}")
        step_ref = request.form.get(f"step-ref-{step}")
        step_existing_img = request.form.get(f"step-existing-img-{step}")
        step_img = request.files[f"step-img-{step}"]

        if step_img != None and crud.allowed_file(step_img.filename):
            filename = secure_filename(step_img.filename)
            step_img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            step_img.close()
        elif step_existing_img:
            filename = step_existing_img
        else:
            filename = "toolbox.png"

        step_data[step] = {}
        step_data[step]["id"] = step_id
        step_data[step]["order"] = step_order
        step_data[step]["text"] = step_text
        step_data[step]["ref"] = step_ref
        step_data[step]["img"] = filename

    crud.update_procedure(proc_id, title, label, cars, tool_data, part_data, step_data)

    return redirect(f"/procedure/{proc_id}")


@app.route("/tool/<tool_id>")
def show_tool_page(tool_id):
    """Render a tool page."""

    user = User.query.filter_by(user_id=session["current_user"]).first()
    tool = Tool.query.filter_by(tool_id=tool_id).first()
    proc_tools = set(ProcedureTool.query.filter_by(tool=tool).all())

    return render_template("tool.html", tool=tool, user=user, proc_tools=proc_tools)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """Serve an uploaded file."""

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/vehicle/<make>")
def show_make_page(make):
    """Render a page that shows all model years for a given make in the db."""

    user = User.query.filter_by(user_id=session["current_user"]).first()
    cars = Car.query.filter_by(make=make).all()
    model_years = set(sorted([car.model_year for car in cars]))

    return render_template(
        "veh-make.html", make=make, model_years=model_years, user=user
    )


@app.route("/vehicle/<make>/<model_year>")
def show_model_year_page(make, model_year):
    """Render a page that shows all cars in db with given make/MY."""

    user = User.query.filter_by(user_id=session["current_user"]).first()
    cars = Car.query.filter(Car.make == make, Car.model_year == model_year).all()
    models = set(sorted([car.model for car in cars]))

    return render_template(
        "veh-make-my.html", make=make, model_year=model_year, models=models, user=user
    )


@app.route("/vehicle/<make>/<model_year>/<model>")
def show_model_page(make, model_year, model):
    """Render a page that shows all procedures for a given vehicle."""

    user = User.query.filter_by(user_id=session["current_user"]).first()
    car = Car.query.filter(
        Car.make == make, Car.model_year == model_year, Car.model == model
    ).first()

    proc_cars = ProcedureCar.query.filter_by(car_id=car.car_id).all()

    return render_template(
        "veh-make-my-model.html",
        user=user,
        proc_cars=proc_cars,
        make=make,
        model_year=model_year,
        model=model,
    )


@app.route("/vehicle-select.json", methods=["POST"])
def select_vehicle():

    model_year = request.form.get("modelYear")
    make = request.form.get("make")
    model = request.form.get("model")

    vehicle_specs = {"model_year": model_year, "make": make, "model": model}

    session["model_year"] = model_year
    session["make"] = make
    session["model"] = model
    print("***************", session["model_year"], session["make"], session["model"])

    return jsonify(vehicle_specs)


@app.route("/write-procedure")
def write_procedure():
    """Render the write-procedure template using existing Part/Tool objects."""

    if session:
        user = User.query.filter_by(user_id=session["current_user"]).first()
        tools = Tool.query.all()
        parts = Part.query.all()
        sorted_makes = crud.get_all_rockauto_makes()

        return render_template(
            "write-procedure.html",
            tools=tools,
            parts=parts,
            sorted_makes=sorted_makes,
            user=user,
        )
    else:
        return redirect("/")


@app.route("/new-fom-send", methods=["POST"])
def alt_form_json_send():

    data = request.form.get_json()
    print(data)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
