from flask import Flask, render_template, redirect
from flask import request, flash, session

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

    return render_template('procedure.html',
                            procedure = procedure,
                            proc_car_obj = proc_car_obj,
                            proc_part_obj = proc_part_obj,
                            proc_tool_obj = proc_tool_obj)


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

    # First, create a new page.
    new_page = crud.create_page(9.99,'newpath22','procedure')

    # Next, take the form data to create a procedure.
    proc_title = request.form.get('proc_title')
    proc_description = request.form.get('proc_text')
    proc_label = request.form.get('proc_label')
    proc_img = request.form.get('proc_img')

    #######################################################
    ### I need to attach a user to this! Need a session!###
    #######################################################
    
    # DELETE LATER.
    new_user = crud.create_user('newusername22', 'newpass', 'newname', 'nada')
    
    new_proc = crud.create_procedure(proc_title,
                                    proc_description,
                                    proc_label,
                                    proc_img,
                                    new_user,
                                    new_page
                                    )

#     # Then, check if the user selected an existing car.
#     # If they did, then keep it handy, and don't create a new Car object.
#     # If they didn't, then double-check that the car is actually new.
#     # If it isn't, then select the corresponding existing car.
#     # Otherwise. create a new Car object with the new info.
#     car_req = request.form.get('car_req')
    
#     if car_req != 'other':
#         car_info = car_req.split('-')
#         car_model_year = int(car_info[0])
#         car_make = car_info[1]
#         car_model = car_info[2]
#         car = Car.query.filter_by(model_year = car_model_year) \
#                 .filter_by(make = car_make).filter_by(model = car_model).one()
#     else:
#         car_model_year = request.form.get('car_model_year')
#         car_make = request.form.get('car_make')
#         car_model = request.form.get('car_model')

#         if Car.query.filter_by(model_year = car_model_year) \
#                 .filter_by(make = car_make).filter_by(model = car_model).one() \
#                 != None:
#             car = Car.query.filter_by(model_year = car_model_year) \
#                 .filter_by(make = car_make).filter_by(model = car_model).one()
#         else:
#             car = crud.create_car(car_model, car_make, car_model_year)
        
#         crud.create_procedure_car(new_proc, car)

#     # Now, check if the user selected an existing tool.
#     # If they did, then keep it handy, and don't create a new Tool object.
#     # If they didn't, then double-check that the tool is actually new.
#     # If it isn't, then select the corresponding existing tool.
#     # Otherwise. create a new Tool object with the new info.
#     # Do this three times.
#     first_tool_req = request.form.get('first_tool_req')

#     if first_tool_req != 'other':
#         tool1 = Tool.query.filter_by(name = first_tool_req).one()
#     else:
#         tool_name = request.form.get('first_tool_other')
#         tool1 = crud.create_tool(tool_name)


#     second_tool_req = request.form.get('second_tool_req')

#     if second_tool_req != 'other':
#         tool2 = Tool.query.filter_by(name = second_tool_req).one()
#     else:
#         tool_name = request.form.get('second_tool_other')
#         tool2 = crud.create_tool(tool_name)


#     third_tool_req = request.form.get('third_tool_req')

#     if third_tool_req != 'other':
#         tool3 = Tool.query.filter_by(name = third_tool_req).one()
#     else:
#         tool_name = request.form.get('third_tool_other')
#         tool3 = crud.create_tool(tool_name)

#     crud.create_procedure_tool(new_proc, tool1)
#     crud.create_procedure_tool(new_proc, tool2)
#     crud.create_procedure_tool(new_proc, tool3)

#     # Now, check if the user selected an existing part.
#     # If they did, then keep it handy, and don't create a new Part object.
#         # This will also require a new PartNumber object.
#     # If they didn't, then double-check that the part is actually new.
#     # If it isn't, then select the corresponding existing part.
#     # Otherwise. create a new Part object with the new info.
#     # Do this three times.
#     first_part_req = request.form.get('first_part_req')

#     if first_part_req != 'other':
#         part1 = Part.query.filter_by(name = first_part_req).one()
#     else:
#         first_part_other_num = request.form.get('first_part_other_num')
#         first_part_other_manuf = request.form.get('first_part_other_manuf')
#         oem1 = request.form.get('oem1')
#         first_part_other_name = request.form.get('first_part_other_name')

#         crud.create_part_num(first_part_other_manuf,
#                              first_part_other_num,
#                              oem1,
#                              first_part_other_name)
        
#         part1 = crud.create_part(first_part_other_name, 'newpath')


#     second_part_req = request.form.get('second_part_req')

#     if second_part_req != 'other':
#         part2 = Part.query.filter_by(name = second_part_req).one()
#     else:
#         second_part_other_num = request.form.get('second_part_other_num')
#         second_part_other_manuf = request.form.get('second_part_other_manuf')
#         oem2 = request.form.get('oem2')
#         second_part_other_name = request.form.get('second_part_other_name')

#         crud.create_part_num(second_part_other_manuf,
#                              second_part_other_num,
#                              oem2,
#                              second_part_other_name)
        
#         part2 = crud.create_part(second_part_other_name, 'newpath')

    
#     third_part_req = request.form.get('third_part_req')

#     if third_part_req != 'other':
#         part3 = Part.query.filter_by(name = third_part_req).one()
#     else:
#         third_part_other_num = request.form.get('third_part_other_num')
#         third_part_other_manuf = request.form.get('third_part_other_manuf')
#         oem3 = request.form.get('oem3')
#         third_part_other_name = request.form.get('third_part_other_name')

#         crud.create_part_num(third_part_other_manuf,
#                              third_part_other_num,
#                              oem3,
#                              third_part_other_name)
        
#         part3 = crud.create_part(third_part_other_name, 'newpath')
    
#     crud.create_procedure_partpart(new_proc, part1)
#     crud.create_procedure_part(new_proc, part2)
#     crud.create_procedure_part(new_proc, part3)

    return render_template('/procedure.html',
                            new_user = new_user,
                            new_page = new_page,
                            new_proc = new_proc
                            )





if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug = True, host = '0.0.0.0')