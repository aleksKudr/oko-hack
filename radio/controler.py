#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2, time
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import serial
ser = serial.Serial("COM3", 9600)
status = 0
print ("Starting program")
while True:
	c=ser.readline()
	print(c)
		
'''		
		print(c)
		if c == b'load\n':
			print(c)
			print ("Start loading\n")
			status = 1
			print (status)
			continue
		else:
			print(c)
	if status == 1:
		c=ser.readline()
		if c != b'load\n':
			print ("Filename: ")
			print(c)
			status = 2
			continue
		
	if status == 2:
		num = []
		i = 0
		while True:
			f2=open("3.jpg","ab")
			c=ser.read(1024)
			i = i+1
			print (i)
			f2.write(c)
			f2.close()
''' 
