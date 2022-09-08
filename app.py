from flask import Flask, render_template, send_from_directory, session, g
from flask_migrate import Migrate
from flask_compress import Compress
from blueprint.article import article_blue
from blueprint.user import user_blue
from admin.admin import admin_blue
from exts import db, mail
from models import User, Nav
import configs
import os

app = Flask(__name__)
Compress(app)
app.config.from_object(configs)
app.register_blueprint(user_blue)
app.register_blueprint(admin_blue)
app.register_blueprint(article_blue)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


@app.template_filter('ellipsis')
def do_ellipsis(arg):
    import re
    return re.sub(r"<.*?>", '', arg)


@app.template_filter('draft_num')
def do_draft_num(arg):
    num = 0
    for i in arg:
        if i.draft:
            num += 1
    return num


@app.template_filter('draft_ex')
def do_draft_ex(arg):
    args = []
    for i in arg:
        if not i.draft:
            args.append(i)
    return args


@app.before_request
def before_request():
    uid = session.get('uid')
    username = session.get('username')
    email = session.get('email')
    if uid and username and email:
        try:
            user = User.query.get(uid)
            g.user = user
        except:
            g.user = None


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {"user": g.user}
    else:
        return {}


@app.context_processor
def context_processor():
    navs = Nav.query.all()
    return {'nav_headers': navs}


@app.errorhandler(Exception)
def catch_all_except():
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
