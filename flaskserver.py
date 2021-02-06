
# Flask
from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    escape,
    request
)

# Random
from os import urandom


app = Flask(__name__)
app.secret_key = urandom(16)


@app.route("/")
def index():
    return  "Hello World"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host= '0.0.0.0')