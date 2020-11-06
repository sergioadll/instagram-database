from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    VIDEO = 1
    PHOTO = 2

follows = db.Table('follows',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('following_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last = db.Column(db.String(80), unique=False, nullable=False)

    posts = db.relationship('Post',backref='user', lazy=True)
    comments = db.relationship('Comment',backref='user', lazy=True)

    following = db.relationship(
        'User', 
        lambda: follows,
        primaryjoin=lambda: User.id == follows.c.user_id,
        secondaryjoin=lambda: User.id == follows.c.following_id,
        backref='followers'
        )

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last": self.last,
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))    

    medias = db.relationship('Media',backref='post', lazy=True)
    comments = db.relationship('Comment',backref='post', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_type = db.Column(db.Enum(MediaType), default=MediaType.PHOTO, nullable=False)
    url = db.Column(db.String(120), unique=False, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))    



    def __repr__(self):
        return '<User %r>' % self.url

    def serialize(self):
        return {
            "id": self.id,
            ##"media_type": self.media_type,
            "url": self.url,
        }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(400), unique=False, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))    
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))    

    def __repr__(self):
        return '<User %r>' % self.comment

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
        }
