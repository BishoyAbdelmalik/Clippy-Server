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

def run_flask():
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
            caller_ip=request.remote_addr
            print(caller_ip)
            file_path=request.args.get("f")
            # folder=os.path.realpath(__file__)+"/static/" 
            print(file_path)
            return send_file(file_path, as_attachment=True)
        except FileNotFoundError:
            abort(404)
    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r
    return app

if __name__ == "__main__":
    app = run_flask()
    app.run(debug=True,host= '0.0.0.0')
    
