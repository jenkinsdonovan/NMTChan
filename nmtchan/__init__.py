"""
TODO: Make "parent" SQL field a string, containing comma separated
    parents to the comment, allowing one comment to be a reply to 
    many. Or, add a table holding holding post relationships. I.e, 
    column 1 is post ID, column 2 is parent ID.
"""

from flask import Flask, send_from_directory
from nmtchan import config, db, index, login, board, post, mod
import os

# declare application
app = Flask(__name__, instance_relative_config=True, template_folder='../templates')
app.config.from_object(config.Config)
app.config['DATABASE'] = os.path.join(app.instance_path, 'nmtchan.sqlite')
app.config['MEDIA_FOLDER'] = os.path.join(app.instance_path, 'media/')
app.config['STATIC_FOLDER'] = os.path.join('../static')

# initialize application
db.init_app(app)

# routes
app.register_blueprint(index.bp)
app.register_blueprint(login.bp)
app.register_blueprint(board.bp)
app.register_blueprint(post.bp)
app.register_blueprint(mod.bp)

@app.route("/static/<f>")
def handleStatic(f):
    return send_from_directory(app.config['STATIC_FOLDER'], f)

@app.route("/instance/media/<f>")
def handleMedia(f):
    return send_from_directory(app.config['MEDIA_FOLDER'], f)