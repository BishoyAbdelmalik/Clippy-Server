# Flask
import json
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
    abort,
    flash
)
import logging
import flask

from werkzeug.utils import secure_filename
import webbrowser
import shutil
from helper import create_dir_if_missing, is_port_in_use
# Random
from os import urandom
import os

def run_flask():
    """Run Flask"""
    app = Flask(__name__)
    app.secret_key = urandom(16)

    logging.basicConfig(filename="logs/flask.log",level=logging.DEBUG)
    
    app.config['UPLOAD_FOLDER'] = 'upload'
    @app.route("/")
    def index():
        return render_template('index.jinja',title="Homepage")
                
    @app.route("/get",methods=["GET"])
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
    @app.route("/recieve",methods=["GET","POST"])
    def recieve():
        if request.method == 'POST':
            print(request.files)
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                abort(404)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                abort(404)
            if file:
                create_dir_if_missing(app.config['UPLOAD_FOLDER'])
                filename = secure_filename(file.filename)
                
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                absolute_path= os.path.join(os.getcwd(), os.path.join(app.config['UPLOAD_FOLDER'], filename))
                webbrowser.open("http://localhost:5000/recieve?f="+absolute_path)

                return "sent"
            abort(500)
        elif request.method=='GET':
            to_be_delete_files(request.args.get("f"))
            return send() 
        else:
            abort(404)
    def to_be_delete_files(path):
        # save files to be deleted in a list that will run on a schedule 
        print(path)
        pass
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
    create_dir_if_missing("config")
    config_path="config/flask.json"
    if os.path.exists( app.config['UPLOAD_FOLDER']):
        shutil.rmtree( app.config['UPLOAD_FOLDER'])
    
    port=5000
    if os.path.exists(config_path):
        loaded_machine_info=json.load(open(config_path,"r"))
        port = loaded_machine_info["port"]
    while is_port_in_use(port):
        port=port+1
    with open(config_path,"w") as f:
        print(json.dumps({"port":port}),file=f)
        f.close()
    app.run(debug=True,host= '0.0.0.0',port=port)
    
