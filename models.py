import app
db = app.db
from datetime import datetime

class Freelancer(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(50))
    contact = db.Column(db.String(50))
    skills = db.Column(db.String(500))
    dob = db.Column(db.Date)
    status = db.Column(db.String(200))
    email = db.Column(db.String(200),unique=True) #to be changed to the propper fields
    password = db.Column(db.String(200)) #to be changed to the propper fields

    def __init__(self, firstname, lastname, contact, skills, dob, status, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.contact = contact
        self.skills = skills
        self.dob = datetime.strptime(dob,'%d-%m-%Y').date()
        self.status = status
        self.email = email
        self.password = password
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Job_postings(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    amount = db.Column(db.Float)
    title = db.Column(db.String(100))
    description = db.Column(db.String(50))
    duration = db.Column(db.String(200)) #to be changed to the propper fields
    no_of_people = db.Column(db.Integer) #to be changed to the propper fields
    posted_by = db.Column(db.Integer,
        nullable=False)


    def __init__(self, posted_by, amount, title, description, duration, no_of_people):
        self.posted_by = posted_by
        self.amount = amount
        self.title = title
        self.description = description
        self.duration = duration
        self.no_of_people = no_of_people


