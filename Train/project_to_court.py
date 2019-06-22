import os 
import csv
import cv2
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mplimg
from pylab import *
from PIL import Image
from skimage import feature, color, transform, io

name = "3.WS _ TAI Tzu Ying (TPE) [1] vs Akane YAMAGUCHI (JPN) [2] _ BWF 2018 (odiasongs.online)"
ext = ".mp4"
filename = name + ext

def swap( a, b ):
    return b, a

def tellme(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()

def zoom_plot():
    happy = False
    while not happy:
        tellme('Select two corners of zoom, middle mouse button to finish')
        pts = np.asarray(ginput(2, timeout=-1))

        happy = len(pts) < 2
        if happy:
            break

        pts = np.sort(pts, axis=0)
        plt.axis(pts.T.ravel())
        plt.gca().invert_yaxis()

def get_point():
    # get mouse clicks
    pts = ginput(n=1,show_clicks=True)
    return pts

def get_rectangle(im):
    points = list()
    for i in range(4):
        # Create figure
        fig2 = plt.figure()
        plt.get_current_fig_manager().full_screen_toggle()  
        plt.imshow(im)
        zoom_plot()
        tellme('Click left-top/right-top/right-down/left-down corner of the square in order.')   
        pts = get_point()
        points.append(list(pts[0]))
        plt.close(fig2)
    return points

def plot_res(im, src, dest, name):
    pts1 = np.float32(src)
    pts2 = np.float32(dest)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    res = cv2.warpPerspective(im,M,(np.float32(1000),np.float32(1800)))

    img_path='./'+name+'.jpg'
    mplimg.imsave(img_path,res)
    return M

def PerspectiveTransform(image, points, dest):
    rows,cols = image.shape[:2]
    # if cols > rows:
    #     maxv = cols
    # else:
    #     maxv = rows 
    M = plot_res(image, points, dest, 'new_image')
    return M

def invertPoint(M, dest,crop_point):
    inv_point=[]
    M_inv = np.linalg.inv(M)

    image = io.imread('./new_image.jpg')
    plt.imshow(image)
    ax = plt.gca()
    ax.xaxis.set_ticks_position('top')
    for p0,p1 in crop_point:
        plt.plot(p0,p1,'ro')
    plt.show()

    for point in crop_point:
        w = 1 / (M_inv[2,0]*point[0] + M_inv[2,1]*point[1] + M_inv[2,2])
        
        x = (M_inv[0,0]*point[0] + M_inv[0,1]*point[1] + M_inv[0,2])*w
        y = (M_inv[1,0]*point[0] + M_inv[1,1]*point[1] + M_inv[1,2])*w
        wx = (M_inv[2,0]*point[0] + M_inv[2,1]*point[1] + M_inv[2,2])*w

        inv_point.append([x,y])
    #print('Crop points: ', crop_point)
    #print('Revert crop points: ', inv_point)
    return M_inv, inv_point

def show_crop(im, inv_point, point):
    plt.imshow(im)
    plt.plot(point[0], point[1], 'bo')
    for i in range(len(inv_point)):
        if i == len(inv_point)-1:
            plt.plot([inv_point[i][0],inv_point[0][0]],[inv_point[i][1],inv_point[0][1]],'r-')
        else:
            plt.plot([inv_point[i][0],inv_point[i+1][0]],[inv_point[i][1],inv_point[i+1][1]],'r-')
    ax = plt.gca()
    ax.xaxis.set_ticks_position('top')
    plt.savefig('./crop.jpg')
    plt.show()

def judge(M_inv,point, crop_point):
    x = (M[0,0]*point[0] + M[0,1]*point[1] + M[0,2])/(M[2,0]*point[0] + M[2,1]*point[1] + M[2,2])
    y = (M[1,0]*point[0] + M[1,1]*point[1] + M[1,2])/(M[2,0]*point[0] + M[2,1]*point[1] + M[2,2])
    #if x >= crop_point[0][0] and x <= crop_point[1][0] and y >= crop_point[0][1] and y <= crop_point[2][1]:
        #return True
    #return False
    #return x, y
    #print(x, y)

    rx = -1
    ry = -1

    if x <= 0:       rx = 0
    elif x <= 32.2:  rx = 1
    elif x <= 212.1: rx = 2
    elif x <= 392.0: rx = 3
    elif x <= 424.2: rx = 4
    else:            rx = 5

    if abs(y-467.5) <= 140:     ry = 1
    elif abs(y-467.5) <= 277.4: ry = 2
    elif abs(y-467.5) <= 414.6: ry = 3
    elif abs(y-467.5) <= 467.8: ry = 4
    else:                       ry = 5

    return rx, ry

if __name__ == '__main__':

    '''
    Create a frame shortcut
    '''
    cam = cv2.VideoCapture(filename)
    # reading from frame 
    cam.set(1, 9000)
    ret, frame = cam.read()

    if ret:
        name = 'frame.jpg'
        print ('Creating...' + name)

        # writing the extracted images 
        cv2.imwrite(name, frame)
    # Release all space and windows once done 
    cam.release()
    cv2.destroyAllWindows()

    '''
    Produce the marix
    '''
    image_name = "frame.jpg"
    image = io.imread(image_name)
    ## get the corners
    # edges = CannyDetect(image)
    # get_corner = getAvgCorner(edges)
    # get the corner of rectangle by using manual marking
    get_corner = get_rectangle(image)
    print('corners: ', get_corner)
    
    # plot corner
    # ax = plt.gca()
    # ax.xaxis.set_ticks_position('top')
    # plt.imshow(image)
    # for p0,p1 in get_corner:
    #     plt.plot(p0,p1,'r.')
    # plt.show()
    
    # coordinate perspective transform
    #dest = [[get_corner[0][0],get_corner[0][1]],[get_corner[0][0]+610,get_corner[0][1]],[get_corner[0][0]+610,get_corner[0][1]+1340],[get_corner[0][0],get_corner[0][1]+1340]]
    dest = [[0,0],[424,0],[424,935],[0,935]]
    #print('Dest point: ',dest)

    # transform metrix
    M = PerspectiveTransform(image, get_corner, dest)
    #print('transform metrix: \n',M)

    ## revert the crop point
    #scale=80
    #crop_point = [[dest[0][0]-scale,dest[0][1]-scale],[dest[1][0]+scale,dest[1][1]-scale],[dest[2][0]+scale,dest[2][1]+scale],[dest[3][0]-scale,dest[3][1]+scale]]
    crop_point = [[dest[0][0]-36.4,dest[0][1]-57.4],[dest[1][0]+36.4,dest[1][1]-57.4],[dest[2][0]+36.4,dest[2][1]+57.4],[dest[3][0]-36.4,dest[3][1]+57.4]]
    
    M_inv, inv_point = invertPoint(M,dest,crop_point)
    
    '''
    Load from skeleton
    '''
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
    
    # Compute x, y of bounding box midpoint
    data2 = np.zeros(shape=(len(data), 4))
    for i in range(len(data)):
        data2[i][0] = data[i][4] + data[i][6]/2
        data2[i][1] = data[i][5] + data[i][7]/2
        data2[i][2] = data[i][12] + data[i][14]/2
        data2[i][3] = data[i][13] + data[i][15]/2
    data = np.hstack((data, data2[:]))

    for i in range(0, 4):
        data = np.delete(data, 4, 1)

    for i in range(0, 4):
        data = np.delete(data, 8, 1)
    
    # Now data only contains players left right foot coor. and bounding box midpoints
    # Since foot coor. in skeleton is at ankles, need to estimate the distance to floor
    
    for i in range(len(data)):
        for j in range(0, 12):
            if j%2 == 1:
                data[i][j] += 10
    
    s = np.zeros(shape=(len(data), 12))

    for i in range(len(data)):
        for j in range(0, 12):
            if j%2 == 1: # y 
                #s[i][j-1], s[i][j] = data[i][j-1],data[i][j]
                s[i][j-1], s[i][j] = judge(M_inv, [data[i][j-1],data[i][j]], crop_point)

    for i in range(len(data)):
        for j in range(2, 9, 4):
            if j == 3 or j == 7:
                swap(s[i][j-3], s[i][j-1])
                swap(s[i][j-2], s[i][j])
    
    np.savetxt('foot_normalize.csv', s, delimiter = ',')
    
    df = pd.read_csv('foot_normalize.csv', header=None, index_col=None)
    df.columns = ["x_left_direct", "x_left_distance", "x_right_direct", "x_right_distance",
        "y_left_direct", "y_left_distance", "y_right_direct", "y_right_distance", 
        "x_direct", "x_distance", "y_direct", "y_distance"]
    df.to_csv('foot_normalize.csv', index=False)
    
    #print(judge(M_inv, [1249,676], crop_point))
    #show_crop(image, inv_point, [int(px),int(py)])
