from flask import Blueprint, request, render_template, jsonify, redirect, session, g
from werkzeug.utils import secure_filename
from decorations import login_required
from exts import mail, db
from flask_mail import Message
from models import EmailCaptcha, User
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import string
import random
import time
import hashlib
import os

user_blue = Blueprint('user_blue', __name__, url_prefix='/user')


@user_blue.route('/<user_id>', methods=['GET', 'POST'])
def user_home(user_id):
    user = User.query.filter_by(uid_md5=user_id).first()
    if user:
        return render_template('homepage.html', user_model=user)
    else:
        return render_template('404.html'), 404


@user_blue.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('setting.html')


@user_blue.route('/settings/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if request.files.get('file'):
            UP_LOAD = 'static/upload/avatar'
            SAVE_PATH = '/static/upload/avatar'
            DIR = os.path.join(os.getcwd(), UP_LOAD)
            f = request.files.get('file')
            md5 = hashlib.md5()
            img_md5 = 'avatars_' + str(random.random()) + str(time.time())
            md5.update(img_md5.encode('utf-8'))
            img_md5 = md5.hexdigest()
            img_name = str(img_md5) + '.' + secure_filename(f.filename).rsplit('.', 1)[1]
            img_url = os.path.join(DIR, img_name)
            f.save(img_url)
            save_path = os.path.join(SAVE_PATH, img_name)
            user = User.query.filter_by(uid=g.user.uid).first()
            user.avatar = save_path
            db.session.commit()
            return {'code': 0, 'msg': '修改成功！'}
        user = User.query.filter_by(uid=g.user.uid).first()
        if g.user.username == request.form.get('username') and g.user.description == request.form.get('description'):
            return {'code': 1, 'msg': '无改动！'}
        else:
            user.username = request.form.get('username')
            user.description = request.form.get('description')
            db.session.commit()
        return {'code': 0, 'msg': '修改成功！'}
    else:
        return render_template('404.html'), 404


@user_blue.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['uid'] = user.uid
        session['username'] = user.username
        session['email'] = user.email
        return jsonify({"status": 200, "msg": '登录成功！'})
    elif user:
        return jsonify({'status': 404, 'msg': '密码错误！'})
    else:
        return jsonify({'status': 404, 'msg': '用户不存在！'})


@user_blue.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    email_model = User.query.filter_by(email=email).first()
    if email_model:
        return jsonify({"status": 404, "msg": '用户已经存在！'})
    else:
        captcha = request.form.get('captcha')
        captcha_model = EmailCaptcha.query.filter_by(email=email).first()
        if captcha_model and captcha_model.captcha.lower() == str(captcha).lower():
            user_sample = string.ascii_letters + string.digits
            captcha = ''.join(random.sample(user_sample, 16))
            username = 'Secret_' + captcha
            username_model = User.query.filter_by(username=username).first()
            if username_model:
                username = username + str(time.time())
            password = request.form.get('password')
            hash_password = generate_password_hash(password)
            avatar = '/static/upload/default/' + str(random.randint(1, 40)) + '.png'
            description = '暂无描述'
            md5 = hashlib.md5()
            uid_md5 = 'Secret_' + str(random.random()) + str(time.time())
            md5.update(uid_md5.encode('utf-8'))
            uid_md5 = md5.hexdigest()
            user = User(username=username, password=hash_password, email=email,
                        avatar=avatar, description=description,
                        uid_md5=uid_md5, join_time=str(datetime.datetime.now()).split(' ', 1)[0])
            db.session.add(user)
            db.session.commit()
            return jsonify({"status": 200, "msg": '注册成功！'})
        else:
            return jsonify({"status": 404, "msg": '验证码错误！'})


@user_blue.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user_blue.route('/retrieve', methods=['POST'])
def retrieve():
    email = request.form.get('email')
    captcha = request.form.get('captcha')
    user = User.query.filter_by(email=email).first()
    if user:
        captcha_model = EmailCaptcha.query.filter_by(email=email).first()
        if captcha_model and captcha_model.captcha.lower() == str(captcha).lower():
            password = request.form.get('password')
            hash_password = generate_password_hash(password)
            user.password = hash_password
            db.session.commit()
            return jsonify({"status": 200, "msg": '修改成功！'})
        else:
            return jsonify({"status": 404, "msg": '验证码错误！'})
    else:
        return jsonify({"status": 404, "msg": "用户不存在！"})


@user_blue.route('/captcha', methods=['POST'])
def verify_mail():
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    if email:
        verify_code_sample = string.ascii_letters + string.digits
        captcha = ''.join(random.sample(verify_code_sample, 6))
        msg = Message()
        msg.subject = str(subject)
        msg.recipients = [email]
        msg.html = f'<p>{str(message)}</p><p>您的验证码为<strong>{captcha}</strong></p>'
        mail.send(msg)
        captcha_model = EmailCaptcha.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha.lower()
            captcha_model.create_time = datetime.datetime.now()
            db.session.commit()
            return jsonify({'status': 200})
        else:
            captcha_model = EmailCaptcha(captcha=captcha.lower(), email=email)
            db.session.add(captcha_model)
            db.session.commit()
            return jsonify({'status': 200})
    else:
        return jsonify({'status': 404, 'msg': '请先输入邮箱！'})
