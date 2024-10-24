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

class Persons(db.Model):
    __tablename__ = 'persons'
    persona_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    city = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    year_experience = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles_persons.role_id'), nullable=False)
    description = db.Column(db.String(500))

# Таблица roles_persons
class Roles_persons(db.Model):
    __tablename__ = 'roles_persons'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    role_name = db.Column(db.String(50), nullable=False)

# Таблица cities
class Cities(db.Model):
    __tablename__ = 'cities'
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

# Таблица contacts
class Contacts(db.Model):
    __tablename__ = 'contacts'
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('persons.persona_id'), nullable=False)
    value = db.Column(db.String(100), nullable=False)

# Таблица events
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

# Таблица applications
class Applications(db.Model):
    __tablename__ = 'applications'
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    persona = db.Column(db.Integer, db.ForeignKey('persons.persona_id'), nullable=False)
    partner = db.Column(db.Integer, db.ForeignKey('persons.persona_id'), nullable=False)
    other_event = db.Column(db.String(200))
    package = db.Column(db.Integer, db.ForeignKey('packages.package_id'), nullable=False)
    add_Friday = db.Column(db.String(20), nullable=False, default="Пока не знаю")
    add_Sunday = db.Column(db.String(20), nullable=False, default="Пока не знаю")
    excursion = db.Column(db.String(20), nullable=False, default="Пока не знаю")
    bank = db.Column(db.Integer, db.ForeignKey('banks.bank_id'))
    comment = db.Column(db.String(500))

# Таблица packages
class Packages(db.Model):
    __tablename__ = 'packages'
    package_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    event = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    package_name = db.Column(db.String(50), nullable=False)
    preferential_price = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Таблица banks
class Banks(db.Model):
    __tablename__ = 'banks'
    bank_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    bank_name = db.Column(db.String(20), nullable=False)

# Таблица recipients
class Recipients(db.Model):
    __tablename__ = 'recipients'
    recipient_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    bank = db.Column(db.Integer, db.ForeignKey('banks.bank_id'), nullable=False)
    requisites = db.Column(db.String(150), nullable=False)

# Таблица approved_applications
class Approved_applications(db.Model):
    __tablename__ = 'approved_applications'
    approved_application_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    persona = db.Column(db.Integer, db.ForeignKey('persons.persona_id'), nullable=False)
    package = db.Column(db.Integer, db.ForeignKey('packages.package_id'), nullable=False)
    payment = db.Column(db.Integer, db.ForeignKey('recipients.recipient_id'), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('statuses.status_id'), nullable=False)

# Таблица statuses
class Statuses(db.Model):
    __tablename__ = 'statuses'
    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    status_name = db.Column(db.String(30), nullable=False)

# Таблица payment
class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    approved_application = db.Column(db.Integer, db.ForeignKey('approved_applications.approved_application_id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipients.recipient_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
