#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import datetime, os, io

import base64
import PIL.Image as Image

from flask_cors import CORS
import sql_oko

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


app.config['UPLOAD_FOLDER'] = "/root/OKO/uploads/"
app.config['MAX_CONTENT_PATH'] = 1024*1024*1024*1024


@app.route('/update_status/', methods=['post'])
def update_status():
	if request.method == 'POST':
		nomer_train = request.form.get('nomer_train') 
		status = request.form.get('status')
		print (nomer_train)
		print (status)
		if(sql_oko.update_status(nomer_train, status)):
			return "OK"
		else:
			return "NO"
	else:
		return "NO"
		
		
@app.route('/get_train_info/', methods=['post'])
def get_train_info():
	if request.method == 'POST':
		nomer_train = request.form.get('nomer_train') 
		print (nomer_train)
		try:
			message = sql_oko.get_train_info(nomer_train)
			print (message)
		except:
			message = "NO"
		return message
	else:
		return "NO"
		
@app.route('/update_train_info/', methods=['post'])
def update_train_info():
	if request.method == 'POST':
		try:
			nomer_train = request.form.get('nomer_train') 
			procent = request.form.get('procent') 
			link1 = request.form.get('photo_number') 
			link2 = request.form.get('photo_real') 
			link3 = request.form.get('photo_cv') 
			print (nomer_train)
			sql_oko.update_train_info(nomer_train, procent, link1, link2, link3)
			message = "OK"
			print (message)
		except:
			message = "NO"
		return message
	else:
		return "NO"
		
		
@app.route('/get_status/', methods=['post', 'get'])
def get_status():
	message = ''
	if request.method == 'GET':
		#message = '[{"id_order":"2", "nomer_train":"9500001", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"На хранении", "update":"11:30"}, {"id_order":"3", "nomer_train":"9500002", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"На хранении", "update":"12:30"}, {"id_order":"4", "nomer_train":"9500003", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"На разгрузке", "update":"13:30"}, {"id_order":"5", "nomer_train":"9500004", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"На разгрузке", "update":"14:30"}, {"id_order":"6", "nomer_train":"9500005", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"На разгрузке", "update":"15:30"}, {"id_order":"7", "nomer_train":"9500006", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"Приемка", "update":"16:30"}, {"id_order":"8", "nomer_train":"9500007", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"Приемка", "update":"17:30"}, {"id_order":"9", "nomer_train":"9500008", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"На хранении", "update":"18:30"}, {"id_order":"10", "nomer_train":"9500009", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"На хранении", "update":"19:30"}]'
		try:
			message = sql_oko.get_all_status()
		except:
			message = "NO"
		return message
	if request.method == 'POST':
		provider = request.form.get('provider') 
		print (provider)
		#if provider == 'popov':
		# -->> SELECT * FROM status WHERE username = 'ИП Попов А.С'
		try:
			message = sql_oko.get_statusbar(provider)
		except:
			message = "NO"
		return message
	else:
		return "NO"
		
	
		
@app.route('/provider/', methods=['post', 'get'])
def provider_login():
	message = ''
	if request.method == 'GET':
		return render_template('provider.html', message=message)
	if request.method == 'POST':
		username = request.form.get('username') 
		password = request.form.get('password')
		print (username)
		print (password)
	if username == 'popov' and password == 'qwerty123':
		message = "Correct username and password" #JSON
		return render_template('provider.html', message=message)
		#return "OK"
	else:
		message = "Wrong username or password"
		return message
	return render_template('provider.html', message=message)

@app.route('/login/', methods=['post', 'get'])
def login():
	message = ''
	if request.method == 'POST':
		username = request.form.get('username') 
		password = request.form.get('password')
		print (username)
		print (password)
	if username == 'admin' and password == 'qwerty123':
		message = "Correct username and password"
		return "OK"
	else:
		message = "Wrong username or password"
		return "NO"
	#return render_template('login.html', message=message)

@app.route('/upload_image/', methods=['post', 'get'])
def upload_image():
	message = ''
	if request.method == 'POST':
		photo = request.form.get('photo') 
		print (photo)
		image = Image.open(io.BytesIO(base64.b64decode(photo)))
		image.save('test.png')
		try:
			with open('/root/OKO/uploads/encode.jpg', "wb") as file:
				file.write(photo)
			return "OK"
		except:
			return "NO"
	else:
		message = "Wrong username or password"
		return "NO"
	
	
@app.route('/upload')
def upload_file():
	return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
		return 'file uploaded successfully'


@app.route("/")
def hello():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {'title' : 'OKO!', 'time': timeString}
	return render_template('index.html', **templateData)
   

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
