from exts import db
import datetime


class EmailCaptcha(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.Integer, unique=True)
    captcha = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid_md5 = db.Column(db.String(255), unique=True, index=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=0)
    avatar = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True, default='暂无描述')
    join_time = db.Column(db.String(255), nullable=False)
    ban = db.Column(db.Boolean, default=False)
    gold = db.Column(db.Integer, default=0)
    exts = db.relationship('UserExts', backref='user', uselist=False)
    articles = db.relationship('Article', backref='user')
    comments = db.relationship('Comment', backref='user')
    replys = db.relationship('Reply', backref='user')
    three_replys = db.relationship('ThreeReply', backref='user')


class UserExts(db.Model):
    __tablename__ = 'userexts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))


like = db.Table(
    'like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.uid')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.aid')))

shoucang = db.Table(
    'shoucang',
    db.Column('user_id', db.Integer, db.ForeignKey('user.uid')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.aid')))


class Article(db.Model):
    __tablename__ = 'article'
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aid_md5 = db.Column(db.String(255), unique=True, index=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    cover = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    sort = db.relationship('Sort', backref='article')
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='article')
    draft = db.Column(db.Boolean, default=False)
    add_time = db.Column(db.DateTime, default=datetime.datetime.now())
    shoucang_users = db.relationship(
        'User',
        secondary=shoucang,
        backref=db.backref('shoucangs', lazy="dynamic"),
        lazy="dynamic"
    )
    like_users = db.relationship(
        'User',
        secondary=like,
        backref=db.backref('likes'),
        lazy="dynamic"
    )


ar_t = db.Table(
    'ar_t',
    db.Column('article_id', db.Integer, db.ForeignKey('article.aid')),
    db.Column('tag_tid', db.Integer, db.ForeignKey('tag.tid')))


class Tag(db.Model):
    __tablename__ = 'tag'
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tagname = db.Column(db.String(255), unique=True, index=True)
    articles = db.relationship(
        'Article',
        secondary=ar_t,
        backref=db.backref('tags', lazy="dynamic"),
        lazy="dynamic"
    )
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())


class Sort(db.Model):
    __tablename__ = 'sort'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sortname = db.Column(db.String(255), unique=True, index=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.aid'))


comment_like = db.Table(
    'comment_like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.uid')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.cid')))


class Comment(db.Model):
    __tablename__ = 'comment'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    username = db.Column(db.String(255))
    likes = db.Column(db.Integer, default=0)
    notlikes = db.Column(db.Integer, default=0)
    article_id = db.Column(db.Integer, db.ForeignKey('article.aid'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    replys = db.relationship('Reply', backref='comment')
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    like_users = db.relationship(
        'User',
        secondary=comment_like,
        backref=db.backref('comment_likes', lazy="dynamic"),
        lazy="dynamic"
    )


class Reply(db.Model):
    __tablename__ = 'reply'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    username = db.Column(db.String(255))
    likes = db.Column(db.Integer, default=0)
    notlikes = db.Column(db.Integer, default=0)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.cid'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())


class ThreeReply(db.Model):
    __tablename__ = 'threereply'
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    username = db.Column(db.String(255))
    likes = db.Column(db.Integer, default=0)
    notlikes = db.Column(db.Integer, default=0)
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.rid'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())


class Nav(db.Model):
    __tablename__ = 'nav'
    nid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    navname = db.Column(db.String(255), unique=True, index=True)
    url = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
