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

    return render_template('homepage.html',
                            procedures = procedures)


@app.route('/procedure')
def show_procedure_page():
    """Render a procedure page."""

    return render_template('procedure.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug = True, host = '0.0.0.0')