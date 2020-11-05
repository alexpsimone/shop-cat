from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def show_landing():
    """Render the Shop Cat landing page.
    
    This may eventually turn into a login page."""

    return render_template('shopcat.html')


@app.route('/home')
def show_homepage():
    """Render the homepage."""

    return render_template('homepage.html')


@app.route('/procedure')
def show_procedure_page():
    """Render a procedure page."""

    return render_template('procedure.html')


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')