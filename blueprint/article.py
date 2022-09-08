from flask import Blueprint, render_template, g, jsonify, request
from werkzeug.utils import secure_filename
from decorations import login_required
from exts import db
from models import Article, User, Comment, Reply
import hashlib
import random
import time
import os
import datetime

article_blue = Blueprint('article_blue', __name__, url_prefix='/article')


@article_blue.route('/<article_id>')
def article(article_id):
    article_model = Article.query.filter_by(aid_md5=article_id).first()
    if article_model.draft:
        return render_template('404.html'), 404
    else:
        article_model.views += 1
        if hasattr(g, 'user'):
            check = article_model.like_users.filter_by(uid=g.user.uid).first()
        else:
            check = None
        db.session.commit()
        return render_template('article.html', article_model=article_model, check=check)


@article_blue.route('/<article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article_model = Article.query.filter_by(aid_md5=article_id).first()
    if request.method == 'GET':
        if article_model:
            if g.user == article_model.user:
                return render_template('write.html')
            return render_template('404.html'), 404
        else:
            return render_template('404.html'), 404
    else:
        if article_model:
            if g.user == article_model.user:
                return jsonify({'status': 200, 'title': article_model.title, 'content': article_model.content})
            return jsonify({'status': 404, 'msg': '错误！'})
        else:
            return jsonify({'status': 404, 'msg': '错误！'})


@article_blue.route('/<article_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(article_id):
    article_model = Article.query.filter_by(aid_md5=article_id).first()
    if request.method == 'GET':
        return render_template('404.html'), 404
    else:
        if article_model:
            if g.user == article_model.user:
                comments = article_model.comments
                for comment in comments:
                    db.session.delete(comment)
                db.session.delete(article_model)
                db.session.commit()
                return jsonify({'status': 200, 'msg': '删除成功！'})
            return jsonify({'status': 404, 'msg': '删除失败！'})
        else:
            return jsonify({'status': 404, 'msg': '错误！'})


@article_blue.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        if hasattr(g, 'user'):
            return render_template('write.html')
        else:
            return jsonify({'status': 404, 'msg': '请先登录！'})
    else:
        if hasattr(g, 'user'):
            return render_template('write.html')
        else:
            return render_template('404.html'), 404


@article_blue.route('/write/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        UP_LOAD = 'static/upload/article'
        SAVE_PATH = '/static/upload/article'
        DIR = os.path.join(os.getcwd(), UP_LOAD)
        f = request.files.get('f')
        md5 = hashlib.md5()
        img_md5 = 'images_' + str(random.random()) + str(time.time())
        md5.update(img_md5.encode('utf-8'))
        img_md5 = md5.hexdigest()
        img_name = str(img_md5) + '.' + secure_filename(f.filename).rsplit('.', 1)[1]
        img_url = os.path.join(DIR, img_name)
        f.save(img_url)
        save_path = os.path.join(SAVE_PATH, img_name)
        return {'img_url': save_path, 'filename': img_name}
    else:
        return render_template('404.html'), 404


@article_blue.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    if request.method == 'GET':
        return render_template('404.html'), 404
    else:
        if request.form.get('id') == '1':
            title = request.form.get('title')
            content = request.form.get('content')
            length = request.form.get('length')
            if len(title) == 0:
                return jsonify({'status': 404, 'msg': '保存失败，标题为空！'})
            elif len(title) > 100:
                return jsonify({'status': 404, 'msg': '保存失败，标题过长！'})
            if int(length) < 10:
                return jsonify({'status': 404, 'msg': '保存失败，字数不足！'})
            if request.form.get('aid'):
                aid_md5 = request.form.get('aid')
                article_model = Article.query.filter_by(aid_md5=aid_md5).first()
                article_model.title = title
                article_model.content = content
                article_model.add_time = datetime.datetime.now()
                article_model.draft = True
            else:
                md5 = hashlib.md5()
                aid_md5 = 'Write_' + str(random.random()) + str(time.time())
                md5.update(aid_md5.encode('utf-8'))
                aid_md5 = md5.hexdigest()
                add_time = datetime.datetime.now()
                article_model = Article(title=title, content=content, author_id=g.user.uid, aid_md5=aid_md5,
                                        add_time=add_time, draft=True)
                db.session.add(article_model)
            db.session.commit()
            return jsonify({'status': 200, 'msg': '保存成功！'})
        elif request.form.get('id') == '2':
            title = request.form.get('title')
            content = request.form.get('content')
            length = request.form.get('length')
            if len(title) == 0:
                return jsonify({'status': 404, 'msg': '发布失败，标题为空！'})
            elif len(title) > 100:
                return jsonify({'status': 404, 'msg': '发布失败，标题过长！'})
            if int(length) < 10:
                return jsonify({'status': 404, 'msg': '发布失败，字数不足！'})
            if request.form.get('aid'):
                aid_md5 = request.form.get('aid')
                article_model = Article.query.filter_by(aid_md5=aid_md5).first()
                article_model.title = title
                article_model.content = content
                article_model.add_time = datetime.datetime.now()
                article_model.draft = False
            else:
                md5 = hashlib.md5()
                aid_md5 = 'Write_' + str(random.random()) + str(time.time())
                md5.update(aid_md5.encode('utf-8'))
                aid_md5 = md5.hexdigest()
                add_time = datetime.datetime.now()
                article_model = Article(title=title, content=content, author_id=g.user.uid, aid_md5=aid_md5,
                                        add_time=add_time)
                db.session.add(article_model)
            db.session.commit()
            return jsonify({'status': 200, 'msg': '发布成功！', 'id': aid_md5})


@article_blue.route('/<article_id>/like', methods=['GET', 'POST'])
def like(article_id):
    if request.method == 'POST':
        if hasattr(g, 'user'):
            article_model = Article.query.filter_by(aid_md5=article_id).first()
            user = article_model.like_users.filter_by(uid=g.user.uid).first()
            if user:
                article_model.like_users.remove(user)
                article_model.likes -= 1
            else:
                article_model.like_users.append(g.user)
                article_model.likes += 1
            db.session.commit()
            return jsonify({'status': 200, 'msg': '感谢点赞！'})
        else:
            return jsonify({'status': 404, 'msg': '请先登录！'})
    else:
        return render_template('404.html'), 404


@article_blue.route('/<article_id>/comment', methods=['GET', 'POST'])
def comment(article_id):
    if request.method == 'POST':
        if hasattr(g, 'user'):
            if len(request.form.get('content')) == 0:
                return jsonify({'status': 404, 'msg': '请先输入评论！'})
            if request.form.get('id') == str(1):
                content = request.form.get('content')
                article_model = Article.query.filter_by(aid_md5=article_id).first()
                article_id = article_model.aid
                user = User.query.filter_by(uid=g.user.uid).first()
                user_id = user.uid
                username = user.username
                add_time = datetime.datetime.now()
                comment_model = Comment(content=content, article_id=article_id, user_id=user_id,
                                        username=username, add_time=add_time)
                db.session.add(comment_model)
                db.session.commit()
            elif request.form.get('id') == 2:
                content = request.form.get('content')
                user = User.query.filter_by(uid=g.user.uid).first()
                user_id = user.uid
                username = user.username
                reply_model = Reply(content=content, user_id=user_id, username=username)
                reply_model.comment.append()
                db.session.add(reply_model)
                db.session.commit()
            elif request.form.get('id') == 3:
                pass
            return jsonify({'status': 200, 'msg': '评论成功！'})
        else:
            return jsonify({'status': 404, 'msg': '请先登录！'})
    else:
        return render_template('404.html'), 404


@article_blue.route('/<article_id>/comment/like', methods=['GET', 'POST'])
def commen_like(article_id):
    if request.method == 'POST':
        if hasattr(g, 'user'):
            comment_id = request.form.get('comment_id')
            comment_model = Comment.query.filter_by(cid=comment_id).first()
            user = comment_model.like_users.filter_by(uid=g.user.uid).first()
            if user:
                comment_model.like_users.remove(user)
                comment_model.likes -= 1
            else:
                comment_model.like_users.append(g.user)
                comment_model.likes += 1
            db.session.commit()
            return jsonify({'status': 200, 'msg': '感谢点赞！'})
        else:
            return jsonify({'status': 404, 'msg': '请先登录！'})
    else:
        return render_template('404.html'), 404
