from flask import Flask, url_for, render_template, redirect, request
from model import *
from datetime import datetime
import os
from PIL import Image
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import secrets

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd7bc5c1e79754cd01beee7ca22d3d93'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'gov_login'
login_manager.login_message_category = 'info'
engine = create_engine('sqlite:///conduent.db',connect_args={'check_same_thread': False}
, echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

@login_manager.user_loader
def load_user(id):
	return session.query(Government).get(int(id))

@app.route('/home')
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/bid')
def bid():
	now = datetime.now()
	tender = session.query(Tender).all()
	return render_template('bid.html', tenders=tender, time = now)

@app.route('/contractor/register', methods=['GET', 'POST'])
def cont_reg():
	if request.method == 'POST':
		address = request.form.get('id')
		password = request.form.get('password')
		registration_pic = request.form.get('uploadImage')
		tax_certificate = request.form.get('uploadImage1')
		contractor = Contrator(address = address, password = password, registration_pic = registration_pic, tax_certificate = tax_certificate)
		session.add(contractor)
		session.commit()
		return redirect(url_for('cont_login'))
	return render_template('cont.html')

@app.route('/create/contract', methods=['GET', 'POST'])
@login_required
def create():
	if request.method == 'POST':
		# government_id=request.form.get('id')
		tender_category=request.form.get('catagory')
		tender_start_date=request.form.get('opening_date')
		tender_start_date = datetime.strptime(tender_start_date, '%Y-%m-%d')
		tender_close_date=request.form.get('closing_date')
		tender_close_date = datetime.strptime(tender_close_date, '%Y-%m-%d')
		# tender_smart_contract_address =request.form.get('add_contract')
		# government = session.query(Government).filter(Government.address == '0x7668EA42D882f72486a34fCcAF7E9bA8A16135c9').first()
		# 0x58d10d1fbba1b0a6ff703e3dfb101a1b0169cdcc
		# 0xC1aB9e7feedB0e91D7a88FBD7951F26c0a0c2829
		# 0x4215c9f53fdff66e1d6ba57068476d5469d27218
		tender=Tender(tender_smart_contract_address = '0xC1aB9e7feedB0e91D7a88FBD7951F26c0a0c2829',tender_category=tender_category,tender_start_date=tender_start_date,tender_close_date=tender_close_date, owner = current_user)
		session.add(tender)
		session.commit()
		logout_user()
		return redirect(url_for('home'))
	return render_template('createContract.html')

@app.route('/government/register', methods=['GET', 'POST'])
def gov_reg():
	if request.method =='POST':
		address=request.form.get('id')
		password=request.form.get('password')
		id_proof=request.form.get('document')
		government=Government(address=address,password=password,id_proof=id_proof)
		session.add(government)
		session.commit()
		return redirect(url_for('gov_login'))
	return render_template('gov.html')

@app.route('/governemnt/functions')
def gov_func():

	return render_template('govMainPage.html')

@app.route('/contractor/login', methods=['GET', 'POST'])
def cont_login():
	if request.method=='POST':
		address=request.form.get('id')
		password = request.form.get('password')
		user=session.query(Contrator).filter(Contrator.address==address).first()
		if user and user.password==password:
			return redirect(url_for('bid'))
		else:
			return redirect(url_for('cont_login'))
	return render_template('log_cnt.html')

@app.route('/government/login', methods=['GET', 'POST'])
def gov_login():
	if request.method == 'POST':
		address = request.form.get('id')
		password = request.form.get('password')
		authenticate_user = session.query(Government).filter(Government.address == address).first()
		# user = session.query(Government).filter(Government.address == address).first()
		if authenticate_user and authenticate_user.password == password:
			login_user(authenticate_user)
			return redirect(url_for('gov_func'))
		else:
			return redirect(url_for('gov_login'))
	return render_template('log_gov.html')

@app.route('/tenders/info')
def tenders():
	now = datetime.now()
	tender = session.query(Tender).all()
	return render_template('tenders.html', tenders = tender, time = now)

@app.route('/update/contract', methods=['GET', 'POST'])
@login_required
def update():
	if request.method == 'POST':
		address = request.form.get('id')
		end_date = request.form.get('closing_date')
		end_date = datetime.strptime(end_date, '%Y-%m-%d')
		user = session.query(Tender).filter(Tender.tender_smart_contract_address == address).first()
		user.tender_close_date = end_date
		session.commit()
		logout_user()
		return redirect(url_for('home'))
	return render_template('updateContract.html')

@app.route('/verifier/login', methods=['GET', 'POST'])
def ver_login():
	if request.method=='POST':
		Username=request.form.get('id')
		password=request.form.get('password')
		user=session.query(Verifier).filter(Verifier.Username==Username).first()
		if(user and user.password == password):
			return redirect(url_for('ver_contractor'))
		else:
			return redirect(url_for('ver_login'))
	return render_template('verifier.html')

@app.route('/verify/contractor')
def ver_contractor():
	return render_template('verifierMain.html')

if __name__ == '__main__':
	app.run(debug = True)
