import os
import psycopg2
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from werkzeug.utils import secure_filename


app = Flask(__name__)
Mobility(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Qwerty1!@localhost:5432/tangobd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'persons'
    persona_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    year_experience = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles_persons.role_id'), nullable=False)
    description = db.Column(db.String(500))

    contacts = db.relationship('Contact', backref='person')
    applications_person = db.relationship('Application', foreign_keys='Application.persona_id', backref='person')
    applications_partner = db.relationship('Application', foreign_keys='Application.partner_id', backref='partner')

class RolePerson(db.Model):
    __tablename__ = 'roles_persons'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    role_name = db.Column(db.String(50), nullable=False)

class City(db.Model):
    __tablename__ = 'cities'
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

class Contact(db.Model):
    __tablename__ = 'contacts'
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('persons.persona_id'), nullable=False)
    value = db.Column(db.String(100), nullable=False)

class Events(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    date_start_registr = db.Column(db.Date, nullable=False)
    date_up_price = db.Column(db.Date, nullable=False)
    date_refund_half = db.Column(db.Date, nullable=False)
    date_refund_lack = db.Column(db.Date, nullable=False)

    packages = db.relationship('Package', backref='event')

class Application(db.Model):
    __tablename__ = 'applications'
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('persons.persona_id'), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('persons.persona_id'), nullable=False)
    other_event = db.Column(db.String(200))
    package_id = db.Column(db.Integer, db.ForeignKey('packages.package_id'), nullable=False)
    add_Friday = db.Column(db.String(20), default="Пока не знаю", nullable=False)
    add_Sunday = db.Column(db.String(20), default="Пока не знаю", nullable=False)
    excursion = db.Column(db.String(20), default="Пока не знаю", nullable=False)
    bank_text = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    amount = db.Column(db.Float)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipients.recipient_id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.status_id'), nullable=False)

class Package(db.Model):
    __tablename__ = 'packages'
    package_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    package_name = db.Column(db.String(50), nullable=False)
    preferential_price = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Bank(db.Model):
    __tablename__ = 'banks'
    bank_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    bank_name = db.Column(db.String(20), nullable=False)

class Recipient(db.Model):
    __tablename__ = 'recipients'
    recipient_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.bank_id'), nullable=False)
    requisites = db.Column(db.String(150), nullable=False)

class Status(db.Model):
    __tablename__ = 'statuses'
    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    status_name = db.Column(db.String(30), nullable=False)

class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipients.recipient_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)


@app.route('/', methods=['POST', 'GET'])
@mobile_template("{mobile/}main.html")
def index(template):
    if request.method == 'POST':
        if request.form['action'] == 'in':
            return redirect('/events')
    else:
        return render_template(template)


@app.route('/events', methods=['POST', 'GET'])
@mobile_template("{mobile/}events.html")
def events(template):
    return render_template(template, id=1)

@app.route('/event/<int:id>/info', methods=['POST', 'GET'])
@mobile_template("{mobile/}event.html")
def event(template, id):
    return render_template(template, id=id)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
