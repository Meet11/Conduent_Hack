from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conduent.db'
db = SQLAlchemy(app)

class Verifier(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	Username = db.Column(db.String)
	password = db.Column(db.String)

class Government(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	address = db.Column(db.String, unique = True)
	password = db.Column(db.String)
	id_proof = db.Column(db.String)
	tender = db.relationship('Tender', backref = 'owner', lazy = 'dynamic')
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return self.id

class Contrator(db.Model):
	address = db.Column(db.String, primary_key = True)
	password = db.Column(db.String)
	registration_pic = db.Column(db.String, unique = True)
	tax_certificate = db.Column(db.String, unique = True)

class Tender(db.Model):
	tender_smart_contract_address = db.Column(db.String, primary_key = True)
	tender_category = db.Column(db.String)
	tender_start_date = db.Column(db.DateTime)
	tender_close_date = db.Column(db.DateTime)
	government_id = db.Column(db.String ,db.ForeignKey('government.id'))