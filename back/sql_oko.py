#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime

def get_ooo(login):
	conn = sqlite3.connect("oko.sqlite")
	cursor = conn.cursor()
	sql = "SELECT location FROM users WHERE login=\'" + login+"\'"
	cursor.execute(sql)
	ooo = (cursor.fetchall()[0][0]) 
	return ooo

def get_statusbar(provider):
	conn = sqlite3.connect("oko.sqlite")
	cursor = conn.cursor()
	#print (provider)
	print (get_ooo(provider))
	sql = "SELECT * FROM statusbar WHERE provider=\'" + get_ooo(provider) +"\'"
	cursor.execute(sql)
	#[{"id_order":"2", "nomer_train":"9500001", "provider":"ИП Попов А.С.", "type_gruz":"Гречиха", "massa":"20", "status":"На хранении", "updater":"11:30"}]
	js = "["
	i = 0
	a = cursor.fetchall()
	#print (a)
	for line in a:
		js = js + "{\"id_order\":\""+str(line[0])+"\", \"nomer_train\":\""+line[1]+"\", \"provider\":\""+line[2]+"\", \"type_gruz\":\""+line[3]+"\", \"massa\":\""+line[4]+"\", \"status\":\""+line[5]+"\", \"updater\":\""+line[6]+"\", \"procent\":\""+line[7]+"\", \"photo_number\":\""+line[8]+"\", \"photo_real\":\""+line[9]+"\", \"photo_cv\":\""+line[10]+"\"},"
	return (js[:-1]+"]")
	
def get_all_status():
	conn = sqlite3.connect("oko.sqlite")
	cursor = conn.cursor()
	sql = "SELECT * FROM statusbar"
	cursor.execute(sql)
	js = "["
	i = 0
	for line in cursor.fetchall():
		js = js + "{\"id_order\":\""+str(line[0])+"\", \"nomer_train\":\""+line[1]+"\", \"provider\":\""+line[2]+"\", \"type_gruz\":\""+line[3]+"\", \"massa\":\""+line[4]+"\", \"status\":\""+line[5]+"\", \"updater\":\""+line[6]+"\", \"procent\":\""+line[7]+"\", \"photo_number\":\""+line[8]+"\", \"photo_real\":\""+line[9]+"\", \"photo_cv\":\""+line[10]+"\"},"
		#print (line)
	return (js[:-1]+"]")
	
def get_status(nomer_train):
	# SELECT status FROM statusbar WHERE nomer_train = '9500000'
	conn = sqlite3.connect("oko.sqlite")
	cursor = conn.cursor()
	sql = "SELECT status FROM statusbar WHERE nomer_train = \'" + nomer_train+"\'"
	cursor.execute(sql)
	status = cursor.fetchall()[0][0]
	return status
	

def update_status(nomer_train, status):
	# UPDATE statusbar SET status = 'Принято', updater='14:00' WHERE nomer_train = '9500000'
	old_status = get_status(nomer_train)
	if status == old_status:
		print ("Nothing. No update")
	else:
		#https://stackoverflow.com/questions/30071886/how-to-get-current-time-in-python-and-break-up-into-year-month-day-hour-minu
		now = datetime.datetime.now()
		updater = ('{:02d}'.format(now.hour)+':'+'{:02d}'.format(now.minute))
		print (nomer_train)
		print (updater)
		conn = sqlite3.connect("oko.sqlite")
		cursor = conn.cursor()
		sql = "UPDATE statusbar SET status = \'"+status+"', updater=\'"+ updater +"\' WHERE nomer_train = \'"+ nomer_train + "\'"
		print(sql)
		cursor.execute(sql)
		conn.commit()
		new_status = get_status(nomer_train)
		print (new_status)
		if new_status == status:
			print("Update succesfull")
			return 1
		else:
			print ("Nothing. No update")
	return 0
	
		
def get_train_info(nomer_train):
	# SELECT * FROM statusbar WHERE nomer_train = '9500000'
	conn = sqlite3.connect("oko.sqlite")
	cursor = conn.cursor()
	sql = "SELECT * FROM statusbar WHERE nomer_train = \'" + nomer_train+"\'"
	cursor.execute(sql)
	line = cursor.fetchall()[0]
	js = "[{\"id_order\":\""+str(line[0])+"\", \"nomer_train\":\""+line[1]+"\", \"provider\":\""+line[2]+"\", \"type_gruz\":\""+line[3]+"\", \"massa\":\""+line[4]+"\", \"status\":\""+line[5]+"\", \"updater\":\""+line[6]+"\", \"procent\":\""+line[7]+"\", \"photo_number\":\""+line[8]+"\", \"photo_real\":\""+line[9]+"\", \"photo_cv\":\""+line[10]+"\"}]"
	#print(js)
	return js
	
def update_train_info(nomer_train, procent, link1, link2, link3):
	try:
		# UPDATE statusbar SET procent = '10', photo_number ='link1', photo_real = 'link2' photo_cv=link3 WHERE nomer_train = '9500000'
		conn = sqlite3.connect("oko.sqlite")
		cursor = conn.cursor()
		sql = "UPDATE statusbar SET procent = \'"+procent+"', photo_number=\'"+ link1 +"\', photo_real=\'"+ link2 +"\', photo_cv=\'"+ link3 + "\' WHERE nomer_train = \'"+ nomer_train + "\'"
		print(sql)
		cursor.execute(sql)
		conn.commit()
		return 1
	except:
		return 0
	
	
def main(args):
	ooo = get_ooo('popov')
	print (get_statusbar(ooo))
	print()
	print(get_all_status())
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
