#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial, time 
import datetime
ser = serial.Serial("/dev/ttyACM0", 9600)

time.sleep(5)
ser.write(b'load\n')
time.sleep(5)
ser.write(b'load\n')
time.sleep(5)
ser.write(b'load\n')


time.sleep(5)
ser.write(b'1.jpg\n')
print ("File opening...")
time.sleep(5)
f = open('2.jpg', 'rb')
content = f.read()
f.close()

#ser.close()

print ("START")
print (len(content))


j = 0
i = 0
num=[]
for c in content:
	num.append(c)
	"""i = i + 1
	if i == 1024:
		i = 0
		j = j + 1
		print (j)
		ser.close()
		num=[]
		time.sleep(20)"""
arr=bytearray(num)
ser.write(arr)
		
print ("FINISH")


ser.write(0x1A)

"""
while True:
	for i in range(0,255):
		ser.write(bytes(str(i), 'utf-8'))
		ser.write(b'\n')
		ser.write(bytes(str(datetime.datetime.now()), 'utf-8'))
		ser.write(b'\n')
		
		time.sleep(5)
		ser.write(b'load\n')
		time.sleep(5)
		ser.write(b'data\n')
		time.sleep(5)
		ser.write(b'finish\n')'''
		time.sleep(1)
		"""
