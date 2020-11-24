from flask import Flask, render_template, redirect, send_from_directory
from flask import request, flash, session, jsonify
from jinja2 import StrictUndefined
from werkzeug.utils import secure_filename
import requests, json
import os

from model import connect_to_db
import crud

app = Flask(__name__)

UPLOAD_FOLDER = 'static/img/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_login():
    """Render the landing/login page."""

    if session:
        return redirect('/home')
    else:
        return render_template('shopcat.html')


@app.route('/build-procedure', methods=["POST"])
def build_procedure():
    """Build a procedure with the info given in the form."""

    # Take the form data to create a Procedure object.
    proc_title = request.form.get('proc_title')
    proc_label = request.form.get('proc_label')

    user = crud.get_user_by_id(session['current_user'])
    
    procedure = crud.create_procedure(proc_title,
                                        proc_label,
                                        user
                                        )

    """
    For each step added by the user, create a Step object.
    Check to see if reference or image checkboxes were selecteed.
    If they were, then look to the corresponding input fields for data.
    Add image and reference info to the Step objects as required.
    """
    NUM_STEPS = int(request.form.get('NUM_STEPS'))

    for step in range(1, (NUM_STEPS + 1)):

        step_text = request.form.get(f'step_text_{step}')
        ref_check = request.form.get(f'ref_{step}')
        
        if ref_check:
            ref_text = request.form.get(f'ref_text_{step}')
            step_img = request.files[f'step_img_{step}']
            if step_img and crud.allowed_file(step_img.filename):
                filename = secure_filename(step_img.filename)
                step_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                step_img.close()
            else:
                filename = 'toolbox.png'
            new_step = crud.create_step(step, 
                                        step_text, 
                                        procedure, 
                                        ref_text,
                                        filename)     
        else:
            ref_text = 'No Ref Provided'
            step_img = request.files[f'step_img_{step}']
            if step_img and crud.allowed_file(step_img.filename):
                filename = secure_filename(step_img.filename)
                step_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                step_img.close()
            else:
                filename = 'toolbox.png'
            new_step = crud.create_step(step, 
                                        step_text, 
                                        procedure,
                                        ref_text,
                                        filename)

    """
    Check if the user selected an existing car.
    If they did, then keep it handy, and don't create a new Car object.
    If they didn't, then use the session info to create one.
    """
    model_year = session['model_year']
    make = session['make']
    model = session['model']

    if crud.get_car_by_details(model_year, make, model):
        car = crud.get_car_by_details(model_year, make, model)
    else:
        car = crud.create_car(model, make, model_year)
        
    # Use the Car and Procedure objects to make a new ProcedureCar.
    crud.create_procedure_car(procedure, car)

    """
    Check if the user selected an existing tool.
    If they did, then keep it handy, and don't create a new Tool object.
    If they didn't, then double-check that the tool is actually new.
    If it isn't, then select the corresponding existing tool.
    Otherwise. create a new Tool object with the new info.
    Then create a corresponding ProcedureTool object.
    Do this for all tools added to the procedure.
    """
    NUM_TOOLS = int(request.form.get('NUM_TOOLS'))
    
    for tool in range(1, (NUM_TOOLS + 1)):
        
        tool_req = request.form.get(f'tool_req_{tool}')
        tool_other = request.form.get(f'tool_other_{tool}')

        if tool_req != 'other':
            my_tool = crud.check_toolbox(tool_req)
        elif crud.check_toolbox(tool_other) != None:
            my_tool = crud.check_toolbox(tool_other)
        else:
            tool_img = request.files[f'tool_img_{tool}']
            if tool_img and crud.allowed_file(tool_img.filename):
                filename = secure_filename(tool_img.filename)
                tool_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                tool_img.close()
            else:
                filename = 'toolbox.png'
            my_tool = crud.create_tool(tool_other, filename)
        
        crud.create_procedure_tool(procedure, my_tool)
     
    """
    Check if the user selected an existing part.
    If they did, then keep it handy, and don't create a new Part object.
    If they didn't, then double-check that the part is actually new.
    If it isn't, then select the corresponding existing part.
    Otherwise. create a new Part object with the new info.
        This will also require a new PartNumber object.
    Then create a corresponding ProcedurePart object.
    Do this for all parts added to the procedure.
    """
    NUM_PARTS = int(request.form.get('NUM_PARTS'))

    for part in range(1, (NUM_PARTS + 1)):
        
        part_req = request.form.get(f'part_req_{part}')
        part_other = request.form.get(f'part_other_{part}')
        
        if part_req != 'other':
            my_part = crud.check_parts_bin(part_req)
        elif crud.check_parts_bin(part_other) != None:
            my_part = check_parts_bin(part_other)
        else:
            part_img = request.files[f'part_img_{part}']
            if part_img and crud.allowed_file(part_img.filename):
                filename = secure_filename(part_img.filename)
                part_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                part_img.close()
            else:
                filename = 'toolbox.png'
            part_other_name = request.form.get(f'part_{part}_other_name')
            part_other_num = request.form.get(f'part_{part}_other_num')
            part_other_manuf = request.form.get(f'part_{part}_other_manuf')
            oem = request.form.get('oem_{part}')
            my_part = crud.create_part(part_other_name, filename)
            crud.create_part_num(part_other_manuf,
                                 part_other_num,
                                 oem,
                                 my_part)
        
        crud.create_procedure_part(procedure, my_part)

    return redirect('/home')


@app.route('/dashboard/<user_id>')
def show_dashboard(user_id):
    """Render the user dashboard."""

    if session:

        user = crud.get_user_by_id(user_id)
        procedures = crud.get_procedures_by_user_id(user_id)
        model_year = session.get('model_year')
        make = session.get('make')
        model = session.get('model')

        return render_template('dashboard.html',
                                user = user,
                                procedures = procedures,
                                model_year = model_year,
                                make = make,
                                model = model)
    else:
        return redirect('/')


@app.route('/edit-procedure/<proc_id>')
def edit_procedure(proc_id):
    """Render the procedure editing form."""

    if session:
        procedure = crud.get_procedure_by_id(proc_id)
        proc_car_obj = crud.get_proc_car_by_proc_id(proc_id)
        proc_part_obj = crud.get_parts_by_proc_id(proc_id)
        proc_tool_obj = crud.get_tools_by_proc_id(proc_id)
        num_tools = crud.num_tools_by_proc(proc_id)
        num_parts = crud.num_parts_by_proc(proc_id)
        num_cars = crud.num_cars_by_proc(proc_id)
        num_steps = crud.num_steps_by_proc(proc_id)
        steps = crud.get_steps_by_proc_id(proc_id)
        sorted_makes = crud.get_all_rockauto_makes()
        
        return render_template('edit-procedure.html',
                                procedure = procedure,
                                proc_car_obj = proc_car_obj,
                                proc_part_obj = proc_part_obj,
                                proc_tool_obj = proc_tool_obj,
                                steps = steps,
                                num_tools = num_tools,
                                num_parts = num_parts,
                                num_cars = num_cars,
                                num_steps = num_steps,
                                sorted_makes = sorted_makes)
    else:
        return redirect('/')

    return render_template('edit-procedure.html')


@app.route('/existing-user', methods = ['POST'])
def login_user():
    """Log in with an existing user account."""

    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if user:
        if user.password == password:
            session['current_user'] = user.user_id
            flash(f'Welcome, {user.username}!')
            return redirect('/home')
        else:
            flash('Password is incorrect.')
            return redirect('/login')
    else:
        flash(f'No account exists with this username')
        return redirect('/login')


@app.route('/get-models.json')
def get_all_models():
    
    all_models = []
    model_year = request.args.get('modelYear')
    make = request.args.get('make')
    # ##########################################################
    # ###TODO: Figure out how to make this PEP-8 compliant!!!###
    # ##########################################################
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeYear/make/{make}/modelyear/{model_year}?format=json'
    res = requests.get(url)
    data = res.json()
    
    for item in data['Results']:
        all_models.append(item['Model_Name'])
    sorted_models = sorted(all_models)

    return jsonify(sorted_models)


@app.route('/get-parts.json')
def get_all_parts():
    """Get all parts from the shopcat database and return as JSON."""

    parts = [part.name for part in crud.get_parts()]

    return jsonify(parts)


@app.route('/get-tools.json')
def get_all_tools():
    """Get all tools from the shopcat database and return as JSON."""

    tools = [tool.name for tool in crud.get_tools()]

    return jsonify(tools)


@app.route('/home')
def show_homepage():
    """Render the homepage."""

    if session: 
        user_id = session['current_user']
        user = crud.get_user_by_id(user_id)
        procedures = crud.get_procedures()
        tools = crud.get_tools()
        cars = crud.get_cars()
        model_years = set([car.model_year for car in cars])
        makes = set([car.make for car in cars])

        return render_template('homepage.html',
                                user = user,
                                procedures = procedures,
                                tools = tools,
                                model_years = model_years,
                                makes = makes)
    else:
        return redirect('/')


@app.route('/login')
def login_page():
    """Render the login page."""

    return render_template('login.html')


@app.route('/new-user', methods = ['POST'])
def new_user():
    """Create a new user."""

    username = request.form.get('username')
    password = request.form.get('password')
    nickname = request.form.get('nickname')

    user = crud.get_user_by_username(username)

    if user:
        flash('A user already exists with that username.')
        return redirect('/')
    else:
        crud.create_user(username, password, nickname)
        flash(f'New account created. Please use your credentials to log in.')
        return redirect('/login') 


@app.route('/procedure/<proc_id>')
def show_procedure_page(proc_id):
    """Render a procedure page."""

    if session:
        procedure = crud.get_procedure_by_id(proc_id)
        proc_car_obj = crud.get_proc_car_by_proc_id(proc_id)
        proc_part_obj = crud.get_parts_by_proc_id(proc_id)
        proc_tool_obj = crud.get_tools_by_proc_id(proc_id)
        steps = crud.get_steps_by_proc_id(proc_id)
        proc_num_tools = crud.num_tools_by_proc(proc_id)
        proc_num_parts = crud.num_parts_by_proc(proc_id)
        
        return render_template('procedure.html',
                                procedure = procedure,
                                proc_car_obj = proc_car_obj,
                                proc_part_obj = proc_part_obj,
                                proc_tool_obj = proc_tool_obj,
                                steps = steps,
                                proc_num_tools = proc_num_tools,
                                proc_num_parts = proc_num_parts)
    else:
        return redirect('/')


@app.route('/rebuild-procedure', methods = ['POST'])
def rebuild_procedure():
    """Rebuild an edited procedure."""

    # Retrieve the procedure to be edited.
    proc_id = int(request.form.get('proc_id'))

    # Retrieve the procedure title.
    title = request.form.get('title')

    # Retrieve the label, if it exists. 
    # Also retrieve whether or not the label is marked for removal.
    remove_label = request.form.get('label-remove')
    label = request.form.get('label')

    # Retrieve all cars listed on the form.
    cars = request.form.getlist('cars')
    
    # Iterate through all tools on the form. Make  a list of tuples (?)
    # containing this information.
    NUM_TOOLS = int(request.form.get('NUM_TOOLS'))
    
    tool_data = []

    for tool in range(1, (NUM_TOOLS + 1)):
        
        tool_id = request.form.get(f'tool-id-{tool}')
        tool_name = request.form.get(f'tool-name-{tool}')
        tool_existing_img = request.form.get(f'tool-existing-img-{tool}')
        tool_img = request.files[f'tool-img-{tool}']
        tool_other = request.form.get(f'tool-other-name-{tool}')

        if tool_img != None and crud.allowed_file(tool_img.filename):
                filename = secure_filename(tool_img.filename)
                tool_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                tool_img.close()
        elif tool_existing_img:
            filename = tool_existing_img
        else:
            filename = 'toolbox.png'

        tool_data.append((tool_id, tool_name, filename, tool_other))
    
    # Iterate through all parts on the form. Make  a list of tuples (?)
    # containing this information.
    NUM_PARTS = int(request.form.get('NUM_PARTS'))
    
    part_data = []

    for part in range(1, (NUM_PARTS + 1)):
        
        part_id = request.form.get(f'part-id-{part}')
        part_name = request.form.get(f'part-name-{part}')
        part_existing_img = request.form.get(f'part-existing-img-{part}')
        part_img = request.files[f'part-img-{part}']
        part_other = request.form.get(f'part-other-name-{part}')
        part_pn = request.form.get(f'part-other-pn-{part}')
        part_manuf = request.form.get(f'part-other-manuf-{part}')
        part_oem = (request.form.get(f'part-other-oem-{part}') == 'True')

        if part_img != None and crud.allowed_file(part_img.filename):
                filename = secure_filename(part_img.filename)
                part_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                part_img.close()
        elif part_existing_img:
            filename = part_existing_img
        else:
            filename = 'toolbox.png'

        part_data.append((part_id, 
                            part_name, 
                            filename, 
                            part_other, 
                            part_pn, 
                            part_manuf, 
                            part_oem))

    # Iterate through all steps on the form. Make  a list of tuples (?)
    # containing this information.
    step_data = []
    NUM_STEPS = int(request.form.get('NUM_STEPS'))

    for step in range(1, (NUM_STEPS + 1)):
        
        step_id = request.form.get(f'step-id-{step}')
        step_order = request.form.get(f'step-order-{step}')
        step_text = request.form.get(f'step-text-{step}')
        step_ref = request.form.get(f'step-ref-{step}')
        step_existing_img = request.form.get(f'step-existing-img-{step}')
        step_img = request.files[f'step-img-{step}']

        if step_img != None and crud.allowed_file(step_img.filename):
                filename = secure_filename(step_img.filename)
                step_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                step_img.close()
        elif step_existing_img:
            filename = step_existing_img
        else:
            filename = 'toolbox.png'
        
        step_data.append((step_id,
                            step_order,
                            step_text,
                            step_ref,
                            filename))

    crud.update_procedure(proc_id, 
                            title, 
                            remove_label, 
                            label,
                            cars,
                            tool_data,
                            part_data,
                            step_data)

    return redirect(f'/edit-procedure/{proc_id}')


@app.route('/tool/<tool_id>')
def show_tool_page(tool_id):
    """Render a tool page."""

    tool = crud.get_tool_by_id(tool_id)

    return render_template('tool.html', tool = tool)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve an uploaded file."""

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/vehicle/<make>')
def show_make_page(make):
    """Render a page that shows all model years for a given make in the db."""

    cars = crud.get_cars_by_make(make)
    model_years = set(sorted([car.model_year for car in cars]))

    return render_template('veh-make.html',
                            make = make, 
                            model_years = model_years)


@app.route('/vehicle/<make>/<model_year>')
def show_model_year_page(make, model_year):
    """Render a page that shows all cars in db with given make/MY."""

    cars = crud.get_cars_by_make_and_model_year(make, model_year)
    models = set(sorted([car.model for car in cars]))

    return render_template('veh-make-my.html',
                            make = make, 
                            model_year = model_year,
                            models = models)


@app.route('/vehicle/<make>/<model_year>/<model>')
def show_model_page(make, model_year, model):
    """Render a page that shows all procedures for a given vehicle."""

    proc_cars = crud.get_proc_car_by_car_info(make, model_year, model)

    return render_template('veh-make-my-model.html',
                            proc_cars = proc_cars,
                            make = make,
                            model_year = model_year,
                            model = model)


@app.route('/vehicle-select', methods=['POST'])
def apply_selected_vehicle():
    """Retrieve selected vehicle info and save to session."""

    model_year = request.form.get('model-year')
    make = request.form.get('make')
    model = request.form.get('model')

    session['model_year'] = model_year
    session['make'] = make
    session['model'] = model
    print('***************', session['model_year'], session['make'], session['model'])

    return redirect('/write-procedure')


@app.route('/vehicle-select.json', methods=['POST'])
def select_vehicle():

    model_year = request.form.get('modelYear')
    make = request.form.get('make')
    model = request.form.get('model')

    vehicle_specs = {'model_year': model_year,
                    'make': make,
                    'model': model
                    }

    session['model_year'] = model_year
    session['make'] = make
    session['model'] = model
    print('***************', session['model_year'], session['make'], session['model'])
    
    return jsonify(vehicle_specs)


@app.route('/write-procedure')
def write_procedure():
    """Render the write-procedure template using existing Part/Tool objects."""

    if session:
        tools = crud.get_tools()
        parts = crud.get_parts()
        sorted_makes = crud.get_all_rockauto_makes()

        return render_template('write-procedure.html',
                                tools = tools,
                                parts = parts,
                                sorted_makes = sorted_makes)
    else:
        return redirect('/')




if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug = True, host = '0.0.0.0')