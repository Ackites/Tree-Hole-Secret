from flask import Blueprint

admin_blue = Blueprint('admin_blue', __name__, url_prefix='/admin')


@admin_blue.route('/login')
def login():
    pass
