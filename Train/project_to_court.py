import csv
import numpy as np
import pandas as pd

def swap( a, b ):
    return b, a

# load frame
framenum = np.array([])
with open('skeleton_data/frame.csv', newline='') as f:
    reader = csv.reader(f)
    next(reader, None)
    c = 0
    for row in reader:
        if c == 0:
            framenum = np.hstack((framenum, np.array(row[:])))
            c = 1
        else:
            framenum = np.vstack((framenum, np.array(row[:])))

# load dataset
data = np.array([])
with open('skeleton_data/top_player_all.csv', newline='') as f:
    reader = csv.reader(f)
    next(reader, None)
    c = 0
    for row in reader:
        for frame_idx in range(len(framenum)):
            if int(framenum[frame_idx]) != int(row[0]):
                continue
            if c == 0:
                data = np.hstack((data, np.array(row[1:])))
                c = 1
            else:
                data = np.vstack((data, np.array(row[1:])))
            frame_idx += 1

frame_idx = 0
data1 = np.array([])
with open('skeleton_data/bot_player_all.csv', newline='') as f:
    reader = csv.reader(f)
    next(reader, None)
    c = 0
    for row in reader:
        for frame_idx in range(len(framenum)):
            if int(framenum[frame_idx]) != int(row[0]):
                continue
            if c == 0:
                data1 = np.hstack((data1, np.array(row[1:])))
                c = 1
            else:
                data1 = np.vstack((data1, np.array(row[1:])))
            frame_idx += 1

data = data.astype(int)
data1 = data1.astype(int)
data = np.hstack((data, data1[:]))

data2 = np.zeros(shape=(len(data), 4))
for i in range(len(data)):
	data2[i][0] = (data[i][0]+data[i][2])/2
	data2[i][1] = (data[i][1]+data[i][3])/2
	data2[i][2] = (data[i][4]+data[i][6])/2
	data2[i][3] = (data[i][5]+data[i][7])/2
data = np.hstack((data, data2[:]))

for i in range(len(data)):
	for j in range(0, 12):
		if j%2 == 1:
			data[i][j] += 15
		elif j%2 == 0:
			data[i][j] += 9

s = np.zeros(shape=(len(data), 12))

for i in range(len(data)):
	for j in range(0, 12):
		if j%2 == 1: # y 
			if data[i][j] >= 669:
				s[i][j] = 5
				if data[i][j-1] >= 1005:
					s[i][j-1] = 5
				elif data[i][j-1] >= 948:
					s[i][j-1] = 4
				elif data[i][j-1] >= 639:
					s[i][j-1] = 3
				elif data[i][j-1] >= 330:
					s[i][j-1] = 2
				elif data[i][j-1] >= 273:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			elif data[i][j] >= 644:
				s[i][j] = 4
				if data[i][j-1] >= 993:
					s[i][j-1] = 5
				elif data[i][j-1] >= 939:
					s[i][j-1] = 4
				elif data[i][j-1] >= 639:
					s[i][j-1] = 3
				elif data[i][j-1] >= 338:
					s[i][j-1] = 2
				elif data[i][j-1] >= 284:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			elif data[i][j] >= 591:
				s[i][j] = 3
				if data[i][j-1] >= 969:
					s[i][j-1] = 5
				elif data[i][j-1] >= 918:
					s[i][j-1] = 4
				elif data[i][j-1] >= 638:
					s[i][j-1] = 3
				elif data[i][j-1] >= 358:
					s[i][j-1] = 2
				elif data[i][j-1] >= 307:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			elif data[i][j] >= 537:
				s[i][j] = 2
				if data[i][j-1] >= 945:
					s[i][j-1] = 5
				elif data[i][j-1] >= 897:
					s[i][j-1] = 4
				elif data[i][j-1] >= 637:
					s[i][j-1] = 3
				elif data[i][j-1] >= 378:
					s[i][j-1] = 2
				elif data[i][j-1] >= 331:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			elif data[i][j] >= 493:
				s[i][j] = 1
				if data[i][j-1] >= 925:
					s[i][j-1] = 5
				elif data[i][j-1] >= 880:
					s[i][j-1] = 4
				elif data[i][j-1] >= 637:
					s[i][j-1] = 3
				elif data[i][j-1] >= 394:
					s[i][j-1] = 2
				elif data[i][j-1] >= 349:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			elif data[i][j] >= 454:
				s[i][j] = 1
				if data[i][j-1] >= 907:
					s[i][j-1] = 5
				elif data[i][j-1] >= 866:
					s[i][j-1] = 4
				elif data[i][j-1] >= 637:
					s[i][j-1] = 3
				elif data[i][j-1] >= 408:
					s[i][j-1] = 2
				elif data[i][j-1] >= 367:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			elif data[i][j] >= 418:
				s[i][j] = 2
				if data[i][j-1] >= 892:
					s[i][j-1] = 5
				elif data[i][j-1] >= 853:
					s[i][j-1] = 4
				elif data[i][j-1] >= 637:
					s[i][j-1] = 3
				elif data[i][j-1] >= 421:
					s[i][j-1] = 2
				elif data[i][j-1] >= 383:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			elif data[i][j] >= 390:
				s[i][j] = 3
				if data[i][j-1] >= 878:
					s[i][j-1] = 5
				elif data[i][j-1] >= 841:
					s[i][j-1] = 4
				elif data[i][j-1] >= 637:
					s[i][j-1] = 3
				elif data[i][j-1] >= 432:
					s[i][j-1] = 2
				elif data[i][j-1] >= 395:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			elif data[i][j] >= 380:
				s[i][j] = 4
				if data[i][j-1] >= 874:
					s[i][j-1] = 5
				elif data[i][j-1] >= 838:
					s[i][j-1] = 4
				elif data[i][j-1] >= 637:
					s[i][j-1] = 3
				elif data[i][j-1] >= 435:
					s[i][j-1] = 2
				elif data[i][j-1] >= 400:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0
			else:
				s[i][j] = 5	
				if data[i][j-1] >= 874:
					s[i][j-1] = 5
				elif data[i][j-1] >= 838:
					s[i][j-1] = 4
				elif data[i][j-1] >= 637:
					s[i][j-1] = 3
				elif data[i][j-1] >= 435:
					s[i][j-1] = 2
				elif data[i][j-1] >= 400:
					s[i][j-1] = 1
				else:
					s[i][j-1] = 0

for i in range(len(data)):
	for j in range(2, 9, 4):
		if j == 3 or j == 7:
			swap(s[i][j-3], s[i][j-1])
			swap(s[i][j-2], s[i][j])

np.savetxt('foot_normalize.csv', s, delimiter = ',')
