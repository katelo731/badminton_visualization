import numpy as np
import cv2
import pickle
from collections import defaultdict
name="TAI Tzu Ying vs CHEN Yufei 2018 Indonesia Open Final  vs"
ext=".mp4"
filename=name+ext
data_position=defaultdict(list)
data_type=defaultdict(set)

total_frame=0
cap = cv2.VideoCapture(filename)
total_frame=cap.get(cv2.CAP_PROP_FRAME_COUNT)
print ("Total frame : "+str(total_frame))

court_map_base=cv2.imread("court.jpg")
court_map=np.copy(court_map_base)

def toggle_set(myset,element):
	if element in myset:
		myset.remove(element)
	else:
		myset.add(element)
def showinfo(n):
	global data_position,data_type
	print(n,data_position[n],data_type[n])
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global data_position,data_type,cap,current
	global image,count_map,court_map_base
	
	if event == cv2.EVENT_LBUTTONDOWN:
		data_position[current]=[x,y]
		toframe(cap,current,total_frame)
		
		# data[current]= (x,y)
		# current+=1
		# image=toframe(cap,current,total_frame)
	if event == cv2.EVENT_RBUTTONDOWN:
		data_position[current]=[]
		toframe(cap,current,total_frame)
		# del data[current]
		# image=toframe(cap,current,total_frame)
	if event==cv2.EVENT_MOUSEWHEEL:
		if flags>0:
			current-=1
		else:
			current+=1
		image=toframe(cap,current,total_frame)
def toframe(cap,n,total_frame):
	global court_map,court_map_base
	showinfo(n)
	cap.set(cv2.CAP_PROP_POS_FRAMES,n);
	ret, frame = cap.read()
	if not ret:
		return None
	else:
		if len(data_position[n])!=0:
			court_map=np.copy(court_map_base)
			cv2.circle(court_map,(data_position[n][0],data_position[n][1]),10,(0,0,0),thickness=3)
		else:
			court_map=np.copy(court_map_base)
		return frame

current=0
image=toframe(cap,current,total_frame)
cv2.namedWindow("image")
cv2.namedWindow("map")
cv2.setMouseCallback("map", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	
	cv2.imshow("image", cv2.resize(image,(0,0),fx=0.5,fy=0.5))
	cv2.imshow("map", court_map)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("f"):
		current=int(input('Enter your frame:'))
		image=toframe(cap,current,total_frame)
	if key == ord("i"):
		current+=3
		image=toframe(cap,current,total_frame)
	if key == ord("t"):
		current-=3
		image=toframe(cap,current,total_frame)
	if key == ord("u"):
		current+=1
		image=toframe(cap,current,total_frame)
	if key == ord("y"):
		current-=1
		image=toframe(cap,current,total_frame)

	if key == ord("k"):
		try:
			pickle.dump(data_position,open(name+"_position.pkl",'wb'))
			pickle.dump(data_type,open(name+"_type.pkl",'wb'))
			print ("saved to "+name+"_position.pkl")
			print ("saved to "+name+"_type.pkl")
		except Exception as e:
			print (str(e))
	if key == ord("l"):
		try:
			data_position=pickle.load(open(name+"_position.pkl",'rb'))
			data_type=pickle.load(open(name+"_type.pkl",'rb'))
			print ("load from "+name+"_position.pkl")
			print ("load from "+name+"_type.pkl")
			max_frame=max(list(data_position.keys()))
			current=max_frame
			toframe(cap,max_frame,total_frame)
		except Exception as e:
			print (str(e))
	# if key == ord("l"):
	# 	try:
	# 		data=pickle.load(open(name+".pkl",'rb'))
	# 		print ("loaded from "+name+".pkl")
	# 		print ("min frame ", str(min(data.keys())))
	# 		print ("max frame ", str(max(data.keys())))
	# 		print ("jump to max frame")
	# 		current=max(data.keys())
	# 		image=toframe(cap,current,total_frame)
	# 	except Exception as e:
	# 		print (str(e))
	# if the 'c' key is pressed, break from the loop
	elif key == ord("m"):
		break
 
# if there are two reference points, then crop the region of interest
# from teh image and display it

 
# close all open windows
cv2.destroyAllWindows()
cap.release()
# for k,v in data.items():
# 	print (k,v)
