import email
from email import charset
from enum import unique
from re import S
from tokenize import String
from flask_sqlalchemy import SQLAlchemy
import datetime
import string
import random

db=SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable = False,unique=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.datetime.now())
    
    bookmarks = db.relationship('Bookmark',backref='user')
    
    def __repr__(self) -> str:
        return f'USER>>> {self.username}, EMAIL>>> {self.email}, PASSWORD>>> {self.password}'
    
class Bookmark(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    url = db.Column(db.Text,nullable = False)
    short_url = db.Column(db.String(3),nullable = False)
    visits = db.Column(db.Integer,default = 0)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime,default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.datetime.now())
    
    def gen_short_char(self):
        charset = string.digits+string.ascii_letters
        selected = ''.join(random.choices(charset,k=3))
        
        dub = self.query.filter_by(short_url=selected).first()
        
        if dub:
            self.gen_short_char()
            
        else:
            return selected
    
    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)
        
        self.short_url = self.gen_short_char()
    
    def __repr__(self) -> str:
        return f'ID>>> {self.id}, BODY>>> {self.body}, URL>>> {self.url}, USER_ID>>> {self.user_id}'