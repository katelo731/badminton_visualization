from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from db import *
from connect import DBconnect
from pynput.keyboard import Key, Controller
import time
import numpy as np
import pymysql
import csv
import sys
import cv2
import math
import threading
from PIL import ImageFont, ImageDraw, Image


connection = DBconnect()
allrally = GetAllRally(connection)
loserally = GetLoseRally(connection,'B')
data = GetRallyPosition(connection,allrally[0][0],allrally[0][1])
btype = GetRallyType(connection,allrally[0][0],allrally[0][1])
arrlen = data.size  
rallyc = 0
rallyl = -1
idc = 0
rev1 = 0
rev2 = 0
#pause = 0

def init():
    glClearColor(1,1,1,1)
    gluOrtho2D(400,0,0,850)   #left, right, bottom, top

def create_GLwindow(size_h,size_w,position_h,position_w,name):
    glutInitWindowSize(size_h,size_w) #height,width 
    glutInitWindowPosition(position_h,position_w)
    glutCreateWindow(name)

def create_CVwindow(size_h,size_w,position_h,position_w,name,img):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(name, position_h,position_w)
    cv2.resizeWindow(name, size_h,size_w)
    cv2.imshow(name, img)

def triangle_coordinate(from_x,from_y,to_x,to_y,point_size):
    coordinate = [[0,0],[0,0],[0,0]]
    point_size = point_size/2 + 0.5
    
    vector = [to_x - from_x , to_y - from_y]
    normal_vector = [-vector[1] , vector[0]]
    dis = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])  
    unit_vector = [vector[0] / dis , vector[1] / dis]
    unit_normal_vector = [normal_vector[0] / dis , normal_vector[1] / dis]

    top = [to_x - unit_vector[0]*point_size , to_y - unit_vector[1]*point_size]
    triangle_size = 10
    mid = [top[0] - unit_vector[0]*triangle_size , top[1] - unit_vector[1]*triangle_size]
    left = [mid[0] + unit_normal_vector[0]*triangle_size , mid[1] + unit_normal_vector[1]*triangle_size]
    right = [mid[0] - unit_normal_vector[0]*triangle_size , mid[1] - unit_normal_vector[1]*triangle_size]

    coordinate = [top,left,right]
    return coordinate

def draw_course():
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth(5)

    glBegin(GL_LINES)
    glColor3f(1,0,0)
    # parallel course line
    glVertex2f(10.0,14.0)
    glVertex2f(378.0,14.0)
    glVertex2f(10.0,60.0)
    glVertex2f(378.0,60.0)
    glVertex2f(10.0,296.0)
    glVertex2f(378.0,296.0)
    glVertex2f(10.0,417.0)
    glVertex2f(378.0,417.0)
    glVertex2f(10.0,538.0)
    glVertex2f(378.0,538.0)
    glVertex2f(10.0,772.0)
    glVertex2f(378.0,772.0)
    glVertex2f(10.0,820.0)
    glVertex2f(378.0,820.0)
    # vertical course line
    glVertex2f(10.0,14.0)
    glVertex2f(10.0,820.0)
    glVertex2f(40.0,14.0)
    glVertex2f(40.0,820.0)
    glVertex2f(195.0,14.0)
    glVertex2f(195.0,296.0)
    glVertex2f(195.0,538.0)
    glVertex2f(195.0,820.0)
    glVertex2f(350.0,14.0)
    glVertex2f(350.0,820.0)
    glVertex2f(378.0,14.0)
    glVertex2f(378.0,820.0)
    glEnd()
    glFlush()
    
def display():
    global data
    global btype
    global rev1
    global rev2
    draw_course()
    
    if rev2 != rev1:
        data = np.flip(data,0)
        btype = btype[::-1]
        print("Reverse!")
    rev1 = rev2

    # mark first ball with black
    glPointSize(20)
    glBegin(GL_POINTS)
    if rev2 == 0:
        glColor3f(0,0,0)
    else:
        glColor3f(0,1,1)
    glVertex2f(data[0][0],data[0][1])
    glEnd()
    glFlush()

    var = 0.95
    for i in range(0,data.shape[0]-1):
        # draw point
        glPointSize(15)
        glBegin(GL_POINTS)
        if btype[i][0] == '切球':
            glColor3f(30/255.,144/255.,255/255.)#blue
        elif btype[i][0] == '放小球' or btype[i][0] == '發小球' or btype[i][0] == '擋小球' or btype[i][0] == '小球':
            glColor3f(138/255.,43/255.,226/255.)#purple
        elif btype[i][0] == '殺球':
            glColor3f(255/255.,0/255.,255/255.)#pink
        elif btype[i][0] == '挑球' or btype[i][0] == '回挑':
            glColor3f(255/255.,130/255.,71/255.)#orange
        elif btype[i][0] == '平球' or btype[i][0] == '小平球':
            glColor3f(128/255.,128/255.,128/255.)#gray
        elif btype[i][0] == '長球':
            glColor3f(139/255.,69/255.,19/255.)#brown
        elif btype[i][0] == '撲球':
            glColor3f(155/255.,205/255.,155/255.)#green
        elif btype[i][0] == '未過網' or btype[i][0] == '未擊球' or btype[i][0] == '掛網球':
            glColor3f(0,0,1)
        glVertex2f(data[i][0],data[i][1])
        glEnd()
        glFlush()

        # draw slowly :)
        time.sleep(0.1)

        # draw line
        glPointSize(2)
        glBegin(GL_POINTS)
        x1,y1 = data[i]
        x2,y2 = data[i+1]
        dx = (x2-x1)/500.0
        dy = (y2-y1)/500.0
        var = var - 1.0/data.size

        if rev2 == 0:
            glColor3f(0,1-var,1-var)
            for i in range(0,250,1):
                glVertex2f(x1+dx*i, y1+dy*i)

            var = var - 1.0/data.size
            glColor3f(0,1-var,1-var)
            for i in range(250,500,1):
                glVertex2f(x1+dx*i, y1+dy*i)
        else:
            glColor3f(0,var,var)
            for i in range(0,250,1):
                glVertex2f(x1+dx*i, y1+dy*i)

            var = var - 1.0/data.size
            glColor3f(0,var,var)
            for i in range(250,500,1):
                glVertex2f(x1+dx*i, y1+dy*i)

        glColor3f(0,0,1)
        glEnd()
        glFlush()

        # draw arrows
        glBegin(GL_TRIANGLES)
        if rev2 == 0:
            glColor3f(0,1-var,1-var)
            coordinate = triangle_coordinate(x1,y1,x2,y2,15)
        else:
            glColor3f(0,var,var)
            coordinate = triangle_coordinate(x2,y2,x1,y1,15)
        glVertex2f(coordinate[0][0],coordinate[0][1])
        glVertex2f(coordinate[1][0],coordinate[1][1])
        glVertex2f(coordinate[2][0],coordinate[2][1])

        glEnd()
        glFlush()

    # mark last ball with blue
    glPointSize(20)
    glBegin(GL_POINTS)
    if rev2 == 0:
        glColor3f(0,1,1)
    else:
        glColor3f(0,0,0)
    glVertex2f(data[data.shape[0]-1][0],data[data.shape[0]-1][1])
    glEnd()
    glFlush()

    # draw last ball
    glPointSize(15)
    glBegin(GL_POINTS)
    if btype[data.shape[0]-1][0] == '切球':
        glColor3f(30/255.,144/255.,255/255.)#blue
    elif btype[data.shape[0]-1][0] == '放小球' or btype[data.shape[0]-1][0] == '發小球' or btype[data.shape[0]-1][0] == '擋小球' or btype[data.shape[0]-1][0] == '小球':
        glColor3f(138/255.,43/255.,226/255.)#purple
    elif btype[data.shape[0]-1][0] == '殺球':
        glColor3f(255/255.,0/255.,255/255.)#pink
    elif btype[data.shape[0]-1][0] == '挑球' or btype[data.shape[0]-1][0] == '回挑':
        glColor3f(255/255.,130/255.,71/255.)#orange
    elif btype[data.shape[0]-1][0] == '平球' or btype[data.shape[0]-1][0] == '小平球':
        glColor3f(128/255.,128/255.,128/255.)#gray
    elif btype[data.shape[0]-1][0] == '長球':
        glColor3f(139/255.,69/255.,19/255.)#brown
    elif btype[data.shape[0]-1][0] == '撲球':
        glColor3f(155/255.,205/255.,155/255.)#green
    elif btype[data.shape[0]-1][0] == '未過網' or btype[data.shape[0]-1][0] == '未擊球' or btype[data.shape[0]-1][0] == '掛網球':
        glColor3f(0,0,1)
    glVertex2f(data[data.shape[0]-1][0],data[data.shape[0]-1][1])
    glEnd()
    glFlush()

def keyboard(bkey, x, y):
    key = bkey.decode("utf-8")
    global rallyc
    global rallyl
    global idc
    global data
    global allrally
    global btype
    global loserally
    global rev2

    if key == 'a' or key == 'A':
        if rallyc==0:
            print("There's no prev2ious rally!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        rallyc=rallyc-1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        glutPostRedisplay()
    if key == 'd' or key == 'D':
        if rallyc>=len(allrally)-1:
            print("There's no next rally!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        rallyc=rallyc+1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        glutPostRedisplay()
    if key == 'w' or key == 'W':
        if(allrally[rallyc][0]=='2018-Indonesia_open-finals-1-1'):
            print("There's no prev2ious game!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        tmp1=str(allrally[rallyc][0])
        while(allrally[rallyc][0]==tmp1 or allrally[rallyc][1]!=str(1)):
            rallyc-=1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        glutPostRedisplay()
    if key == 's' or key == 'S':
        if(allrally[rallyc][0]=='2018-Indonesia_open-finals-1-2'):
            print("There's no next game!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        tmp2=str(allrally[rallyc][0])
        while(allrally[rallyc][0]==tmp2):
            rallyc+=1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        glutPostRedisplay()
    if key == 'h' or key == 'H':
        # print(rallyl)
        if rallyl>=len(loserally)-1:
            print("There's no next rally!")
            print('Here is game:', loserally[rallyl][0], ', rally:', loserally[rallyl][1])
            return
        rallyl=rallyl+1
        data = GetRallyPosition(connection,loserally[rallyl][0],loserally[rallyl][1])
        btype = GetRallyType(connection,loserally[rallyl][0],loserally[rallyl][1])
        if data.shape[0] > 3:
            data = data[-3:]
        if btype.shape[0] > 3:
            btype = btype[-3:]
        print('Here is game:', loserally[rallyl][0], ', rally:', loserally[rallyl][1])
        glutPostRedisplay()
    if key == 'f' or key == 'F':
        # print(rallyl)
        if rallyl == 0:
            print("There's no prev2ious rally!")
            print('Here is game:', loserally[rallyl][0], ', rally:', loserally[rallyl][1])
            return
        rallyl=rallyl-1
        data = GetRallyPosition(connection,loserally[rallyl][0],loserally[rallyl][1])
        btype = GetRallyType(connection,loserally[rallyl][0],loserally[rallyl][1])
        if data.shape[0] > 3:
            data = data[-3:]
        if btype.shape[0] > 3:
            btype = btype[-3:]
        print('Here is game:', loserally[rallyl][0], ', rally:', loserally[rallyl][1])
        glutPostRedisplay()
    if key == 'q' or key == 'Q':
        if rev2 == 0:
            rev2 = 1
        else:
            rev2 = 0
        glutPostRedisplay()
    '''
    if key == ' ':
        if pause==1:
            pause=0
            return
        else:
            pause=1
            return
    '''
'''
def idle():
    global count
    global pause
    time.sleep(0.1)
    if pause == 0:
        count = 0
        #glutPostRedisplay()
'''
def draw_text(img,text,fond_size,position,color):
    fontPath = "./Times_New_Roman_Bold.ttf"         # 指定 TTF 字體檔
    font = ImageFont.truetype(fontPath, fond_size)  # 載入字體

    aPil = Image.fromarray(img)                     # 將 NumPy 陣列轉為 PIL 影像
    draw = ImageDraw.Draw(aPil)                     # 在圖片上加入文字
    draw.text(position,  text, font = font, fill = color)
    img = np.array(aPil)                            # 將 PIL 影像轉回 NumPy 陣列
    
    return img
def show_color_type():
    # Load an type&color image 
    img = cv2.imread('./color2.jpg')
    create_CVwindow(46,150,470,0,'Color',img)
    
def show_player_info():
   
    name_a = 'TAI Tzu Ying'
    a = cv2.imread(str(name_a) + '.jpg')
    cv2.rectangle(a, (0, 516), (560, 646), (255,255,255), -1)
    a = draw_text(a , name_a , 75 , (80,520) , (255,0,0))

    name_b = 'CHEN Yufei'
    b = cv2.imread(str(name_b) + '.jpg')
    cv2.rectangle(b, (0, 516), (560, 646), (255,255,255), -1)
    b = draw_text(b , name_b , 75 , (80,520) , (0,0,0))
    numpy_vertical = np.vstack((a, b))

    create_CVwindow(200,400,470,200,'PlayerInfo',numpy_vertical)
    cv2.waitKey(0)
    cv2.waitKey(0)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    create_GLwindow(400,850,0,0,"Course")

    glEnable(GL_POINT_SMOOTH)
    glutDisplayFunc(display)
    glRotatef(180.0, 0.0, 0.0, 1.0)
    init()
    glutKeyboardFunc(keyboard)
    #glutIdleFunc(idle)
    glutMainLoop()
    
def picture():
    show_color_type()
    show_player_info()

def main_task(): 
  
    # creating threads 
    t1 = threading.Thread(target=main) 
    t2 = threading.Thread(target=picture) 
  
    # start threads 
    t1.start() 
    t2.start() 
  
    # wait until threads finish their job 
    t1.join() 
    t2.join() 

if __name__ == '__main__':
    main_task()