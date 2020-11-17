from flask import Flask, render_template, redirect
from flask import request, flash, session, jsonify
from jinja2 import StrictUndefined
import requests, json

from model import connect_to_db
import crud

app = Flask(__name__)

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
        img_check = request.form.get(f'img_{step}')
        
        if ref_check:
            ref_text = request.form.get(f'ref_text_{step}')
            if img_check:
                step_img = request.form.get(f'img_file_{step}')
                if step_img == '':
                    step_img = 'toolbox.jpg'
                new_step = crud.create_step(step, 
                                            step_text, 
                                            procedure, 
                                            ref_text,
                                            step_img)
            else:
                step_img = 'toolbox.jpg'
                new_step = crud.create_step(step, 
                                            step_text, 
                                            procedure, 
                                            ref_text, 
                                            step_img)      
        else:
            ref_text = 'No Ref Provided'
            if img_check:
                step_img = request.form.get(f'img_file_{step}')
                if step_img == '':
                    step_img = 'toolbox.jpg'
                new_step = crud.create_step(step, 
                                            step_text, 
                                            procedure,
                                            ref_text,
                                            step_img)
            else:
                step_img = 'toolbox.jpg'
                new_step = crud.create_step(step, 
                                            step_text, 
                                            procedure, 
                                            ref_text, 
                                            step_img)

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
            my_tool = crud.create_tool(tool_other)
        
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
            part_other_name = request.form.get(f'part_{part}_other_name')
            part_other_num = request.form.get(f'part_{part}_other_num')
            part_other_manuf = request.form.get(f'part_{part}_other_manuf')
            oem = request.form.get('oem_{part}')
            my_part = crud.create_part(part_other_name, 'newpath')
            crud.create_part_num(part_other_manuf,
                                 part_other_num,
                                 oem,
                                 my_part)
        
        crud.create_procedure_part(procedure, my_part)

    return redirect('/home')


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
    print('********************',model_year,make)
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
        procedures = crud.get_procedures()
        tools = crud.get_tools()
        cars = crud.get_cars()
        model_years = set([car.model_year for car in cars])
        makes = set([car.make for car in cars])

        return render_template('homepage.html',
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

    proc_id = int(request.form.get('proc_id'))
    title = request.form.get('proc-title')

    crud.update_procedure(proc_id, title)

    return redirect(f'/procedure/{proc_id}')


@app.route('/tool/<tool_id>')
def show_tool_page(tool_id):
    """Render a tool page."""

    tool = crud.get_tool_by_id(tool_id)

    return render_template('tool.html', tool = tool)


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
    print('***************', vehicle_specs)

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