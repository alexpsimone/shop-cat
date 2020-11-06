from flask import Flask, render_template, request

from model import connect_to_db
import crud
# from jinja2 import StrictUndefined

app = Flask(__name__)

# app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_landing():
    """Render the Shop Cat landing page.
    
    This may eventually turn into a login page."""

    return render_template('shopcat.html')


@app.route('/home')
def show_homepage():
    """Render the homepage."""

    procedures = crud.get_procedures()
    tools = crud.get_tools()
    parts = crud.get_parts()

    return render_template('homepage.html',
                            procedures = procedures,
                            tools = tools,
                            parts = parts)


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


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug = True, host = '0.0.0.0')