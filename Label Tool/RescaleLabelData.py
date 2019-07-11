import pickle
import math
import cv2
from itertools import islice

name = "2019亞錦賽-周天成VS石宇奇-24"
ext=".mp4"
filename=name+ext

hit = []

try:
	with open(name+"_position.pkl",'rb') as f:
		while True:                          # loop indefinitely
			hit.append(pickle.load(f))       # add each item from the file to a list
except EOFError:                             # the exception is used to break the loop
	pass                                     # we don't need to do anything special

hit = str(hit)
outfile = open(name+'_posfile.csv', 'w')

cap = cv2.VideoCapture(filename)
fps = round(cap.get(cv2.CAP_PROP_FPS))

begin = False
isx = False
isy = False
printf = False
frame = 0
x = 0
y = 0
for i in range(len(hit)):
	if hit[i] == '{':
		begin = True
		continue
	if begin == True:
		if hit[i] == ':' or hit[i] == ' ':
			continue
		if hit[i] == ']' and hit[i-1] == '[':
			frame = 0
			continue
		elif hit[i] == '[' and hit[i+1] != ']':
			isx = True
		elif hit[i] == ',' and isx == True:
			isy = True
			isx = False
		elif hit[i] == ',':
			continue
		elif hit[i] == ']' and hit[i-1] != '[' and isy == True:
			isx = False
			isy = False
			printf = False

			#convert coordinate to area
			if( y == 417):
				if( x < 40):
					area = "D0"	
				if( x >= 40 and x < 105.1):
					area = "B0"
				elif( x >= 105.1 and x < 283.35):
					area = "A0"
				elif( x >= 283.35 and x < 350):
					area = "C0"
				elif( x >= 350):
					area = "E0"
			elif( y < 14):
				if( x < 40):
					area = "D4"	
				if( x >= 40 and x < 105.1):
					area = "B4"
				elif( x >= 105.1 and x < 283.35):
					area = "A4"
				elif( x >= 283.35 and x < 350):
					area = "C4"
				elif( x >= 350):
					area = "E4"
			elif( y < 78.02):
				if( x < 40):
					area = "D3"	
				if( x >= 40 and x < 105.1):
					area = "B3"
				elif( x >= 105.1 and x < 283.35):
					area = "A3"
				elif( x >= 283.35 and x < 350):
					area = "C3"
				elif( x >= 350):
					area = "E3"
			elif( y < 277.98):
				if( x < 40):
					area = "D2"	
				if( x >= 40 and x < 105.1):
					area = "B2"
				elif( x >= 105.1 and x < 283.35):
					area = "A2"
				elif( x >= 283.35 and x < 350):
					area = "C2"
				elif( x >= 350):
					area = "E2"
			elif( y < 417):
				if( x < 40):
					area = "D1"	
				if( x >= 40 and x < 105.1):
					area = "B1"
				elif( x >= 105.1 and x < 283.35):
					area = "A1"
				elif( x >= 283.35 and x < 350):
					area = "C1"
				elif( x >= 350):
					area = "E1"
			elif( y < 556.02):
				if( x < 40):
					area = "E1"	
				if( x >= 40 and x < 105.1):
					area = "C1"
				elif( x >= 105.1 and x < 283.35):
					area = "A1"
				elif( x >= 283.35 and x < 350):
					area = "B1"
				elif( x >= 350):
					area = "D1"
			elif( y < 755.12):
				if( x < 40):
					area = "E2"	
				if( x >= 40 and x < 105.1):
					area = "C2"
				elif( x >= 105.1 and x < 283.35):
					area = "A2"
				elif( x >= 283.35 and x < 350):
					area = "B2"
				elif( x >= 350):
					area = "D2"
			elif( y < 820):
				if( x < 40):
					area = "E3"	
				if( x >= 40 and x < 105.1):
					area = "C3"
				elif( x >= 105.1 and x < 283.35):
					area = "A3"
				elif( x >= 283.35 and x < 350):
					area = "B3"
				elif( x >= 350):
					area = "D3"
			elif( y >= 820):
				if( x < 40):
					area = "E4"	
				if( x >= 40 and x < 105.1):
					area = "C4"
				elif( x >= 105.1 and x < 283.35):
					area = "A4"
				elif( x >= 283.35 and x < 350):
					area = "B4"
				elif( x >= 350):
					area = "D4"

			#rescale coordinate
			if x <= 10: 
				x = x-10
			elif x <= 40: 
				x = (x-10.0)*32.0/30.0
			elif x <= 350: 
				x = (x-40.0)*360.0/310.0+32.0
			else: 
				x = (x-350.0)*32.0/30.0+392.0

			if y <= 14:
				y = y-14
			elif y <= 78.02: 
				y = (y-14.0)*74.0/64.0
			elif y <= 277.98: 
				y = (y-78.02)*233.0/199.96+74.0
			elif y <= 417: 
				y = (y-277.98)*161.0/139.02+307.0
			elif y <= 556.02: 
				y = (y-417.0)*161.0/139.02+468.0
			elif y <= 755.12: 
				y = (y-556.02)*233.0/199.96+629.0
			else:
				y = (y-755.12)*74.0/64.0+861.0

			#x = round(x-36+0.5,0)
			#y = round(y-57+0.5,0)

			outfile.write(str(int(x)))
			outfile.write(',')
			outfile.write(str(int(y)))
			outfile.write(',')
			outfile.write(area)
			outfile.write('\n')
			
			frame = 0
			x = 0
			y = 0
		elif isx == False and isy == False and hit[i].isdigit(): # frame
			frame = frame*10 + int(hit[i])
		elif isx == True and isy == False and hit[i].isdigit() and hit[i-1] != ' ':
			x = x*10 + int(hit[i])
			if printf == False:
				outfile.write(str(frame))
				outfile.write(',')
				frame /= fps
				s = frame % 60
				frame /= 60
				m = frame % 60
				frame /= 60
				h = frame
				outfile.write(str(math.floor(h)))
				outfile.write(':')
				outfile.write(str(math.floor(m)))
				outfile.write(':')
				if s == 0.0:
					s = int(s)
				outfile.write(str(round(s,6)))
				outfile.write(',')
				printf = True
		elif isy == True and hit[i].isdigit():
			y = y*10 + int(hit[i])

outfile.close()
