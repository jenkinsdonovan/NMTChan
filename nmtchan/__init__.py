from flask import Flask, send_from_directory
from nmtchan import db, index, login, board, post, mod, api
import os, json

# declare application
app = Flask(__name__, instance_relative_config=True, template_folder='../templates')
app.config['DATABASE'] = os.path.join(app.instance_path, 'nmtchan.sqlite')
app.config['MEDIA_FOLDER'] = os.path.join(app.instance_path, 'media/')
app.config['STATIC_FOLDER'] = os.path.join('../static')

# load config from file. Create if not exist
try:
    with open("./config.cfg", "r") as f:
        data = json.load(f)
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or data['secret_key']
        app.config['admin'] = data['admin']
except FileNotFoundError:
    print("Creating a config file. Change default values ASAP")
    content = {
        "secret_key":"change_me",
        "admin":{
            "username":"admin",
            "password":"password"
        }
    }
    with open("./config.cfg", "w+") as f:
        f.write(json.dumps(content, indent=4) + "\n")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or content['secret_key']
    app.config['admin'] = content['admin']
except Exception as e:
    print(e)
    exit()

# initialize application
db.init_app(app)

# routes
app.register_blueprint(index.bp)
app.register_blueprint(login.bp)
app.register_blueprint(board.bp)
app.register_blueprint(post.bp)
app.register_blueprint(mod.bp)
app.register_blueprint(api.bp)

@app.route("/static/<f>")
def handleStatic(f):
    return send_from_directory(app.config['STATIC_FOLDER'], f)

@app.route("/instance/media/<f>")
def handleMedia(f):
    return send_from_directory(app.config['MEDIA_FOLDER'], f)