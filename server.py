from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def show_homepage():
    """Render the homepage."""

    return render_template('homepage.html')

@app.route('procedure/')
def show_homepage():
    """Render a procedure page."""

    return render_template('procedure.html')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')