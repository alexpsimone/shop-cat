from flask import Flask, render_template, redirect
from flask import request, flash, session, jsonify

from model import connect_to_db
import crud
import requests, json
from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_landing():
    """Render the Shop Cat landing page.
    
    This may eventually turn into a login page."""

    return render_template('shopcat.html')


@app.route('/login', methods=['POST'])
def login_user():
    """Create a new user or log in existing user."""

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
    else:
        crud.create_user(username, password)
        flash(f'New account created. Please use your credentials to log in.')
        return redirect('/')


@app.route('/home')
def show_homepage():
    """Render the homepage."""

    procedures = crud.get_procedures()

    return render_template('homepage.html', procedures = procedures)


@app.route('/procedure/<proc_id>')
def show_procedure_page(proc_id):
    """Render a procedure page."""

    procedure = crud.get_procedure_by_id(proc_id)
    proc_car_obj = crud.get_proc_car_by_proc_id(proc_id)
    proc_part_obj = crud.get_parts_by_proc_id(proc_id)
    proc_tool_obj = crud.get_tools_by_proc_id(proc_id)
    proc_num_tools = crud.num_tools_by_proc(proc_id)
    
    print("******", proc_tool_obj)

    return render_template('procedure.html',
                            procedure = procedure,
                            proc_car_obj = proc_car_obj,
                            proc_part_obj = proc_part_obj,
                            proc_tool_obj = proc_tool_obj,
                            proc_num_tools = proc_num_tools)


@app.route('/year-make-search')
def show_year_make_search():
    """Render the vehicle year/make search menu."""

    all_makes = []
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json'
    res = requests.get(url)
    data = res.json()

    for item in data['Results']:
        all_makes.append(item['Make_Name'])
    sorted_makes = sorted(all_makes)

    return render_template('year-make-search.html', sorted_makes = sorted_makes)


@app.route('/get-year-make', methods = ["POST"])
def year_make_search():
    
    session['model_year'] = request.form.get('model_year')
    session['make'] = request.form.get('make')

    flash(f"You selected a {session['model_year']} {session['make']}.")

    return redirect('/model-search')


@app.route('/model-search')
def show_model_search():
    """ ."""

    model_year = session['model_year']
    make = session['make']
    all_models = []

    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeYear/make/{make}/modelyear/{model_year}?format=json'
    res = requests.get(url)
    data = res.json()

    for item in data['Results']:
        all_models.append(item['Model_Name'])
    sorted_models = sorted(all_models)

    return render_template('model-search.html', sorted_models = sorted_models)


@app.route('/get-model', methods = ["POST"])
def model_search():
    
    session['model'] = request.form.get('model')

    flash(f"This procedure is written for a {session['model_year']} {session['make']} {session['model']}.")

    return redirect('/write-procedure')


@app.route('/get-tools.json')
def get_all_tools():
    """Get all tools from the database and return as JSON."""

    tools = [tool.name for tool in crud.get_tools()]

    return jsonify(tools)


@app.route('/get-parts.json')
def get_all_parts():
    """Get all parts from the database and return as JSON."""

    parts = [part.name for part in crud.get_parts()]

    return jsonify(parts)


@app.route('/write-procedure')
def write_procedure():

    tools = crud.get_tools()
    parts = crud.get_parts()

    return render_template('write-procedure.html',
                            tools = tools,
                            parts = parts)


@app.route('/build-procedure', methods=["POST"])
def build_procedure():
    """Build a procedure with the info given in the form."""

    # Take the form data to create a procedure.
    proc_title = request.form.get('proc_title')
    proc_description = request.form.get('proc_text')
    proc_label = request.form.get('proc_label')
    proc_img = request.form.get('proc_img')

    user = crud.get_user_by_id(session['current_user'])
    
    procedure = crud.create_procedure(proc_title,
                                        proc_description,
                                        proc_label,
                                        proc_img,
                                        user
                                        )

    # Then, check if the user selected an existing car.
    # If they did, then keep it handy, and don't create a new Car object.
    # If they didn't, then use the session info to create one.

    model_year = session['model_year']
    make = session['make']
    model = session['model']

    if crud.get_car_by_details(model_year, make, model):
        car = crud.get_car_by_details(model_year, make, model)
    else:
        car = crud.create_car(model, make, model_year)
        
    # Use the Car and Procedure objects to make a new ProcedureCar.
    crud.create_procedure_car(procedure, car)

#     # Now, check if the user selected an existing tool.
#     # If they did, then keep it handy, and don't create a new Tool object.
#     # If they didn't, then double-check that the tool is actually new.
#     # If it isn't, then select the corresponding existing tool.
#     # Otherwise. create a new Tool object with the new info.
#     # Do this three times.

    tools = []

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
        
        tools.append(my_tool)
    
    for tool in tools:
        crud.create_procedure_tool(procedure, tool)
     

#     # Now, check if the user selected an existing part.
#     # If they did, then keep it handy, and don't create a new Part object.
#         # This will also require a new PartNumber object.
#     # If they didn't, then double-check that the part is actually new.
#     # If it isn't, then select the corresponding existing part.
#     # Otherwise. create a new Part object with the new info.
#     # Do this three times.

    
    parts = []

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
        
        parts.append(my_part)

    for part in parts:
        crud.create_procedure_part(procedure, part)

    return redirect('/home')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug = True, host = '0.0.0.0')