#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, time

def main(args):
	#r = requests.post('http://oko.hack48.ru:8080/login/', data = {'username':'admin', 'password': 'qwerty123'})  
	##print (r.text)
	#print()
	
	# Получить все данные обо всех вагонах
	print ("GET /get_status/")
	r = requests.get('http://oko.hack48.ru:8080/get_status/')  
	print (r.text)
	print()
	
	# Получить данные о вагонах пользователя с логином popov
	print ("POST /get_status/")
	r = requests.post('http://oko.hack48.ru:8080/get_status/', data = {'provider':'popov'})  
	print (r.text)
	print()
	
	# Изменить статус конкретного вагона (при перезеде или оператор руками)
	# Возможные статусы: "В пути", "На хранении", "На разгрузке", "Приемка", "Принято", "Отказ" // Юля предлагает изменить
	# Отдает в ответ NO - если статус не изменился. Если изменился, то ещё и время там устанавливает.
	print ("POST /update_status/")
	r = requests.post('http://oko.hack48.ru:8080/update_status/', data = {'nomer_train':'9500000','status':'qwerty'})  
	print (r.text)
	print ()
	
	# Получить все данные обо всех вагонах. Посмотреть изменения.
	print ("GET /get_status/")
	r = requests.get('http://oko.hack48.ru:8080/get_status/')  
	print (r.text)
	print ()
	
	# Получить все данные конкретного вагона.
	print ("POST get_train_info")
	r = requests.post('http://oko.hack48.ru:8080/get_train_info/', data = {'nomer_train':'9500000'})  
	print (r.text)
	print ()
	
	# Обновить данные конкретного вагона: процент брака, ссылк на фотографии.
	print ("POST update_train_info")
	r = requests.post('http://oko.hack48.ru:8080/update_train_info/', data = {'nomer_train':'9500000','procent':'10','photo_number':'1.jpg','photo_real':'2.jpg','photo_cv':'3.jpg'})  
	print (r.text)
	print ()
	
	# Получить все данные конкретного вагона - для проверки изменений.
	print ("POST get_train_info")
	r = requests.post('http://oko.hack48.ru:8080/get_train_info/', data = {'nomer_train':'9500000'})  
	print (r.text)
	print ()
	
	return 0
	
	

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
