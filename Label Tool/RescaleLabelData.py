import pickle
import math
from itertools import islice
name = "TAI Tzu Ying vs CHEN Yufei 2018 Indonesia Open Final  vs"

hit = []
try:
	with open(name+"_position.pkl",'rb') as f:
		while True:                          # loop indefinitely
			hit.append(pickle.load(f))       # add each item from the file to a list
except EOFError:                             # the exception is used to break the loop
	pass                                     # we don't need to do anything special

hit = str(hit)
outfile = open('posfile.csv', 'w')

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
				if( x > 10 and x < 40):
					area = "D0"
				elif( x > 40 and x < 195):				
					area = "B0"
				elif( x > 195 and x < 350):
					area = "A0"
				elif( x > 350 and x < 378):
					area = "C0"
			elif( y < 14):
				if( x < 10):		
					area = "F5"				
				elif( x > 10 and x < 40):	
					area = "D5"
				elif( x > 40 and x < 195):
					area = "B5"
				elif( x > 195 and x < 350):				
					area = "A5"
				elif( x > 350 and x < 378):
					area = "C5"
				else:			
					area = "E5"
			elif( y > 820):
				if( x < 10):
					area = "E5"
				if( x > 10 and x < 40):			
					area = "C5"				
				elif( x > 40 and x < 195):			
					area = "A5"				
				elif( x > 195 and x < 350):		
					area = "B5"				
				elif( x > 350 and x < 378):			
					area = "D5"				
				else:			
					area = "F5"			
			elif( x < 10):
				if( y > 14 and y < 60):		
					area = "F4"				
				elif( y > 60 and y < 178):			
					area = "F3"			
				elif( y > 178 and y < 296):
					area = "F2"				
				elif( y > 296 and y < 417):
					area = "F1"				
				elif( y > 417 and y < 538):
					area = "E1"				
				elif( y > 538 and y < 655):			
					area = "E2"				
				elif( y > 655 and y < 772):
					area = "E3"
				elif( y > 772 and y < 820):
					area = "E4"
			elif( x > 378):
				if( y > 14 and y < 60):			
					area = "E4"				
				elif( y > 60 and y < 178):
					area = "E3"				
				elif( y > 178 and y < 296):
					area = "E2"				
				elif( y > 296 and y < 417):
					area = "E1"
				elif( y > 417 and y < 538):
					area = "F1"				
				elif( y > 538 and y < 655):
					area = "F2"
				elif( y > 655 and y < 772):
					area = "F3"				
				elif( y > 772 and y < 820):		
					area = "F4"

			elif( x > 10 and x < 40 and y > 14 and y < 60 ):
				area = "D4"
			elif( x > 10 and x < 40 and y > 60 and y < 178 ):
				area = "D3"
			elif( x > 10 and x < 40 and y > 178 and y < 296 ):
				area = "D2"
			elif( x > 10 and x < 40 and y > 296 and y < 417 ):
				area = "D1"
			elif( x > 10 and x < 40 and y > 417 and y < 538 ):
				area = "C1"
			elif( x > 10 and x < 40 and y > 538 and y < 655 ):
				area = "C2"
			elif( x > 10 and x < 40 and y > 655 and y < 772 ):
				area = "C3"
			elif( x > 10 and x < 40 and y > 772 and y < 820 ):
				area = "C4"
			elif( x > 40 and x < 195 and y > 14 and y < 60 ):
				area = "B4"
			elif( x > 40 and x < 195 and y > 60 and y < 178 ):
				area = "B3"
			elif( x > 40 and x < 195 and y > 178 and y < 296 ):
				area = "B2"
			elif( x > 40 and x < 195 and y > 296 and y < 417 ):
				area = "B1"
			elif( x > 40 and x < 195 and y > 417 and y < 538 ):
				area = "A1"
			elif( x > 40 and x < 195 and y > 538 and y < 655 ):
				area = "A2"
			elif( x > 40 and x < 195 and y > 655 and y < 772 ):
				area = "A3"
			elif( x > 40 and x < 195 and y > 772 and y < 820 ):
				area = "A4"
			elif( x > 195 and x < 350 and y > 14 and y < 60 ):
				area = "A4"
			elif( x > 195 and x < 350 and y > 60 and y < 178 ):
				area = "A3"
			elif( x > 195 and x < 350 and y > 178 and y < 296 ):
				area = "A2"
			elif( x > 195 and x < 350 and y > 296 and y < 417 ):
				area = "A1"
			elif( x > 195 and x < 350 and y > 417 and y < 538 ):
				area = "B1"
			elif( x > 195 and x < 350 and y > 538 and y < 655 ):
				area = "B2"
			elif( x > 195 and x < 350 and y > 655 and y < 772 ):
				area = "B3"
			elif( x > 195 and x < 350 and y > 772 and y < 820 ):
				area = "B4"
			elif( x > 350 and x < 378 and y > 14 and y < 60 ):
				area = "C4"
			elif( x > 350 and x < 378 and y > 60 and y < 178 ):
				area = "C3"
			elif( x > 350 and x < 378 and y > 178 and y < 296 ):
				area = "C2"
			elif( x > 350 and x < 378 and y > 296 and y < 417 ):
				area = "C1"
			elif( x > 350 and x < 378 and y > 417 and y < 538 ):
				area = "D1"
			elif( x > 350 and x < 378 and y > 538 and y < 655 ):
				area = "D2"
			elif( x > 350 and x < 378 and y > 655 and y < 772 ):
				area = "D3"
			elif( x > 350 and x < 378 and y > 772 and y < 820 ):
				area = "D4"
			else:
				area = "yy"
				
			#rescale coordinate
			if x < 0: 
				x = -1
			elif x <= 10: 
				x *= 36.4/10.0
			elif x <= 40: 
				x = (x-10.0)*32.2/30.0+36.4
			elif x <= 195: 
				x = (x-40.0)*179.9/155.0+68.6
			elif x <= 350: 
				x = (x-195.0)*179.9/155.0+248.5
			elif x <= 378: 
				x = (x-350.0)*32.2/28.0+428.4
			elif x <= 388: 
				x = (x-378.0)*36.4/10.0+460.6
			else: 
				x = -1.0

			if y <0:
				y = -1
			elif y <= 14: 
				y *= 57.4/14.0
			elif y <= 60: 
				y = (y-14.0)*53.2/46.0+57.4
			elif y <= 178: 
				y = (y-60.0)*137.2/118.0+110.6
			elif y <= 296: 
				y = (y-178.0)*137.2/118.0+247.8
			elif y <= 417: 
				y = (y-296.0)*140.0/121.0+385.0
			elif y <= 538: 
				y = (y-417.0)*140.0/121.0+525.0
			elif y <= 655: 
				y = (y-538.0)*137.2/117.0+665.0
			elif y <= 772: 
				y = (y-655.0)*137.2/117.0+802.2
			elif y <= 820: 
				y = (y-772.0)*53.2/48.0+939.4
			elif y <= 824: 
				y = (y-820.0)*57.4/14.0+992.6
			else: 
				y = -1.0

			x = round(x-36+0.5,0)
			y = round(y-57+0.5,0)

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
				frame /= 30
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
