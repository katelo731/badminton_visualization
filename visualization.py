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
connection2 = DBconnect()
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
unique_id = allrally[0][0]
rally = 1
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
    var = 0.95
    draw_course()
    
    # data reverse or not
    if rev2 != rev1 or rev2 == 1:
        data = np.flip(data,0)
        btype = btype[::-1]
    rev1 = rev2
    if rev2!=0:
        print("Reverse!")

    # draw
    for i in range(0,data.shape[0]-3,1):
        # draw slowly :)
        time.sleep(0.5)

        line = i
        size = data.size*3
        draw_course()

        for j in range(i,i+4,1):
            if j == 0:
                for k in range(0,3,1):
                    if k == 0:
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
                    else:
                        # draw line
                        glPointSize(2)
                        glBegin(GL_POINTS)
                        x1,y1 = data[k-1]
                        x2,y2 = data[k]
                        dx = (x2-x1)/500.0
                        dy = (y2-y1)/500.0
                        var = var - 1.0/size

                        if rev2 == 0:
                            glColor3f(0,1-var,1-var)
                            for i in range(0,250,1):
                                glVertex2f(x1+dx*i, y1+dy*i)

                            var = var - 1.0/size
                            glColor3f(0,1-var,1-var)
                            for i in range(250,500,1):
                                glVertex2f(x1+dx*i, y1+dy*i)
                        else:
                            glColor3f(0,var,var)
                            for i in range(0,250,1):
                                glVertex2f(x1+dx*i, y1+dy*i)

                            var = var - 1.0/size
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

                    # draw point
                    glPointSize(15)
                    glBegin(GL_POINTS)
                    if btype[k][0] == '切球':
                        glColor3f(30/255.,144/255.,255/255.)#blue
                    elif btype[k][0] == '放小球' or btype[k][0] == '發小球' or btype[k][0] == '擋小球' or btype[k][0] == '小球':
                        glColor3f(138/255.,43/255.,226/255.)#purple
                    elif btype[k][0] == '殺球':
                        glColor3f(255/255.,174/255.,201/255.)#pink
                    elif btype[k][0] == '挑球' or btype[k][0] == '回挑':
                        glColor3f(255/255.,130/255.,71/255.)#orange
                    elif btype[k][0] == '平球' or btype[k][0] == '小平球':
                        glColor3f(170/255.,170/255.,170/255.)#gray
                    elif btype[k][0] == '長球':
                        glColor3f(139/255.,69/255.,19/255.)#brown
                    elif btype[k][0] == '撲球':
                        glColor3f(155/255.,205/255.,155/255.)#green
                    elif btype[k][0] == '未過網' or btype[j][0] == '未擊球' or btype[j][0] == '掛網球':
                        glColor3f(0,0,1)
                    glVertex2f(data[k][0],data[k][1])
                    glEnd()
                    glFlush()
                    time.sleep(0.5)

            # mark last ball with blue
            if j == data.shape[0]-1:
                glPointSize(20)
                glBegin(GL_POINTS)
                if rev2 == 0:
                    glColor3f(0,1,1)
                else:
                    glColor3f(0,0,0)
                glVertex2f(data[data.shape[0]-1][0],data[data.shape[0]-1][1])
                glEnd()
                glFlush()

            # draw point
            glPointSize(15)
            glBegin(GL_POINTS)
            if btype[j][0] == '切球':
                glColor3f(30/255.,144/255.,255/255.)#blue
            elif btype[j][0] == '放小球' or btype[j][0] == '發小球' or btype[j][0] == '擋小球' or btype[j][0] == '小球':
                glColor3f(138/255.,43/255.,226/255.)#purple
            elif btype[j][0] == '殺球':
                glColor3f(255/255.,174/255.,201/255.)#pink
            elif btype[j][0] == '挑球' or btype[j][0] == '回挑':
                glColor3f(255/255.,130/255.,71/255.)#orange
            elif btype[j][0] == '平球' or btype[j][0] == '小平球':
                glColor3f(170/255.,170/255.,170/255.)#gray
            elif btype[j][0] == '長球':
                glColor3f(139/255.,69/255.,19/255.)#brown
            elif btype[j][0] == '撲球':
                glColor3f(155/255.,205/255.,155/255.)#green
            elif btype[j][0] == '未過網' or btype[j][0] == '未擊球' or btype[j][0] == '掛網球':
                glColor3f(0,0,1)
            glVertex2f(data[j][0],data[j][1])
            glEnd()
            glFlush()

            # draw line
            if j > 0 and j != i:
                glPointSize(2)
                glBegin(GL_POINTS)
                x1,y1 = data[j-1]
                x2,y2 = data[j]
                dx = (x2-x1)/500.0
                dy = (y2-y1)/500.0
                var = var - 1.0/size

                if rev2 == 0:
                    glColor3f(0,1-var,1-var)
                    for i in range(0,250,1):
                        glVertex2f(x1+dx*i, y1+dy*i)

                    var = var - 1.0/size
                    glColor3f(0,1-var,1-var)
                    for i in range(250,500,1):
                        glVertex2f(x1+dx*i, y1+dy*i)
                else:
                    glColor3f(0,var,var)
                    for i in range(0,250,1):
                        glVertex2f(x1+dx*i, y1+dy*i)

                    var = var - 1.0/size
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
    global unique_id
    global rally

    if key == 'a' or key == 'A':
        if rallyc==0:
            print("There's no previous rally!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        rallyc=rallyc-1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        unique_id = allrally[rallyc][0]
        rally = allrally[rallyc][1]
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
        unique_id = allrally[rallyc][0]
        rally = allrally[rallyc][1]
        glutPostRedisplay()
    if key == 'w' or key == 'W':
        if(allrally[rallyc][0]=='2018-Indonesia_open-finals-1-1'):
            print("There's no previous game!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        line1=str(allrally[rallyc][0])
        while(allrally[rallyc][0]==line1 or allrally[rallyc][1]!=str(1)):
            rallyc-=1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        unique_id = allrally[rallyc][0]
        rally = allrally[rallyc][1]
        glutPostRedisplay()
    if key == 's' or key == 'S':
        if(allrally[rallyc][0]=='2018-Indonesia_open-finals-1-2'):
            print("There's no next game!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        line2=str(allrally[rallyc][0])
        while(allrally[rallyc][0]==line2):
            rallyc+=1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        unique_id = allrally[rallyc][0]
        rally = allrally[rallyc][1]
        glutPostRedisplay()
    if key == 'h' or key == 'H':
        if rallyl>=len(loserally)-1:
            print("There's no next rally!")
            print('Here is game:', loserally[rallyl][0], ', rally:', loserally[rallyl][1])
            return
        rallyl=rallyl+1
        data = GetRallyPosition(connection,loserally[rallyl][0],loserally[rallyl][1])
        btype = GetRallyType(connection,loserally[rallyl][0],loserally[rallyl][1])
        if data.shape[0] > 4:
            data = data[-4:]
        if btype.shape[0] > 4:
            btype = btype[-4:]
        print('Here is game:', loserally[rallyl][0], ', rally:', loserally[rallyl][1])
        unique_id = loserally[rallyl][0]
        rally = loserally[rallyl][1]
        glutPostRedisplay()
    if key == 'f' or key == 'F':
        if rallyl == 0:
            print("There's no previous rally!")
            print('Here is game:', loserally[rallyl][0], ', rally:', loserally[rallyl][1])
            return
        rallyl=rallyl-1
        data = GetRallyPosition(connection,loserally[rallyl][0],loserally[rallyl][1])
        btype = GetRallyType(connection,loserally[rallyl][0],loserally[rallyl][1])
        if data.shape[0] > 4:
            data = data[-4:]
        if btype.shape[0] > 4:
            btype = btype[-4:]
        print('Here is game:', loserally[rallyl][0], ', rally:', loserally[rallyl][1])
        unique_id = loserally[rallyl][0]
        rally = loserally[rallyl][1]
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
    # Load an type & color image 
    img = cv2.imread('./color2.jpg')
    create_CVwindow(122,248,470,0,'Color',img)

def show_player_info():
    global unique_id
    unique_id = allrally[0][0]
    while(True):
        # load data
        name_upper,player_upper = GetCourtUpper(connection2,unique_id)
        name_lower,player_lower = GetCourtLower(connection2,unique_id)
        score_upper = GetRallyPoints(connection2,unique_id,rally,player_upper)
        score_lower = GetRallyPoints(connection2,unique_id,rally,player_lower)
        # show picture and name
        upper = cv2.imread(str(name_upper) + '.jpg')
        lower = cv2.imread(str(name_lower) + '.jpg')
        cv2.rectangle(upper, (0, 516), (560, 646),(238, 215,143 ) , -1)
        cv2.rectangle(lower, (0, 516), (560, 646), (142, 215,167 ), -1)
        upper = draw_text(upper , name_upper , 75 , (80,520) , (79,24,0))
        lower = draw_text(lower , name_lower , 75 , (80,520) , (8,35,0))
        
        # show score
        if score_upper > score_lower:
            cv2.circle(upper, (470, 430), 68, (0,0,255 ), -1, 8, 0)
            cv2.circle(lower, (470, 430), 68, (0,0,0 ), -1, 8, 0)
        elif score_upper < score_lower:
            cv2.circle(upper, (470, 430), 68, (0,0,0 ), -1, 8, 0)
            cv2.circle(lower, (470, 430), 68, (0,0,255 ), -1, 8, 0)
        else:
            cv2.circle(upper, (470, 430), 68, (40, 144, 255), -1, 8, 0)
            cv2.circle(lower, (470, 430), 68, (40, 144, 255), -1, 8, 0)
        
        upper = draw_text(upper , str(score_upper).rjust(2,' ') , 85 , (430, 385) , (255,255,255 ))
        lower = draw_text(lower , str(score_lower).rjust(2,' ') , 85 , (430, 385) , (255,255,255 ))
        
        numpy_vertical = np.vstack((upper, lower))

        create_CVwindow(140,350,460,300,'PlayerInfo',numpy_vertical)
        cv2.waitKey(1)
   
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
    cv2.waitKey(0)

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
