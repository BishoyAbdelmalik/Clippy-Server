
# Flask
from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    escape,
    request,
    send_file, 
    send_from_directory, 
    safe_join, 
    abort
)

# Random
from os import urandom
import os

app = Flask(__name__)
app.secret_key = urandom(16)


@app.route("/")
def index():
    return  "Hello World"

@app.route("/get")
def send():
    try:
        #TODO only accept from ip connected to websocket 
        #TODO only work if websocket is on
        
        file_path=request.args.get("f")
        # folder=os.path.realpath(__file__)+"/static/" 
        print(file_path)
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host= '0.0.0.0')