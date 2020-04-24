import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('iduser',db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password, name, surname, email):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email


    def completeName(self):
        return self.surname+" "+self.name
    
    def create(self):
        hashPassword = hashlib.new("saralavanchy", self.password)
        db.execute("INSER INTO users (name, surname, username, email, password) VALUES (:name, :surname, :username, :email, :password)", 
            {"name": self.name, "surname" : self.surname, "username" : self.username, "email" : self.email, "password" : hashPassword})
        db.session.commit()
