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
import threading

connection = DBconnect()
allrally = GetAllRally(connection)
loserally = GetLoseRally(connection,'B')
data = GetRallyPosition(connection,allrally[0][0],allrally[0][1])
btype = GetRallyType(connection,allrally[0][0],allrally[0][1])
arrlen = data.size  
rallyc =0
rallyl = -1
idc = 0
path = 0

def init():
    glClearColor(1,1,1,1)
    gluOrtho2D(400,0,0,850)   #left, right, bottom, top

def create_window(size_h,size_w,position_h,position_w,name):
    glutInitWindowSize(size_h,size_w) #height,width 
    glutInitWindowPosition(position_h,position_w)
    glutCreateWindow(name)

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
    global path
    draw_course()

    # mark first ball with green
    glPointSize(20)
    glBegin(GL_POINTS)
    glColor3f(69/255,252/255,185/255)
    glVertex2f(data[0][0],data[0][1])
    glEnd()
    glFlush()

    var=0.95
    for i in range(data.shape[0]-1):
        # draw point
        glPointSize(15)
        glBegin(GL_POINTS)
        if btype[i][0] == '切球':
            glColor3f(30/255.,144/255.,255/255.)#blue
        if btype[i][0] == '放小球' or btype[i][0] == '發小球' or btype[i][0] == '擋小球' or btype[i][0] == '小球':
            glColor3f(138/255.,43/255.,226/255.)#purple
        if btype[i][0] == '殺球':
            glColor3f(255/255.,0/255.,255/255.)#pink
        if btype[i][0] == '挑球' or btype[i][0] == '回挑':
            glColor3f(255/255.,130/255.,71/255.)#orange
        if btype[i][0] == '平球':
            glColor3f(128/255.,128/255.,128/255.)#gray
        if btype[i][0] == '長球':
            glColor3f(139/255.,69/255.,19/255.)#brown
        glVertex2f(data[i][0],data[i][1])
        glEnd()
        glFlush()

        # draw line
        glPointSize(2)
        glBegin(GL_POINTS)
        x1,y1 = data[i]
        x2,y2 = data[i+1]
        dx = (x2-x1)/500.0
        dy = (y2-y1)/500.0

        var=var - 1.0/data.size
        glColor3f(0,1-var,1-var)
        for i in range(0,250,1):
            glVertex2f(x1+dx*i,y1+dy*i)
            time.sleep(0.00000001)

        var=var - 1.0/data.size
        glColor3f(0,1-var,1-var)
        for i in range(250,500,1):
            glVertex2f(x1+dx*i,y1+dy*i)
            time.sleep(0.00000001)

        glColor3f(0,0,1)
        glEnd()
        glFlush()

    # mark last ball with blue
    glPointSize(20)
    glBegin(GL_POINTS)
    glColor3f(0,1,1)
    glVertex2f(data[data.shape[0]-1][0],data[data.shape[0]-1][1])
    glEnd()
    glFlush()

    # draw last ball
    glPointSize(15)
    glBegin(GL_POINTS)
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

    if key == 'a' or key == 'A':
        if rallyc==0:
            print("There's no previous rally!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        rallyc=rallyc-1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        display()
    if key == 'd' or key == 'D':
        if rallyc>=len(allrally)-1:
            print("There's no next rally!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        rallyc=rallyc+1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        display()
    if key == 'w' or key == 'W':
        if(allrally[rallyc][0]=='2018-Indonesia_open-finals-1-1'):
            print("There's no previous game!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        tmp1=str(allrally[rallyc][0])
        while(allrally[rallyc][0]==tmp1 or allrally[rallyc][1]!=str(1)):
            rallyc-=1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        display()
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
        display()
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
        display()
    if key == 'f' or key == 'F':
        # print(rallyl)
        if rallyl == 0:
            print("There's no previous rally!")
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
        display()
'''
def idle():
    global path
    Sleep(20)
    path = (path+1)%500
    display()
'''
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    create_window(400,850,0,0,"Course")

    glEnable(GL_POINT_SMOOTH)
    glutDisplayFunc(display)
    glRotatef(180.0, 0.0, 0.0, 1.0)
    init()
    glutKeyboardFunc(keyboard)
    #glutIdleFunc(idle)
    glutMainLoop()
    
def picture():
    # Load an color image in grayscale
    img = cv2.imread('./color2.jpg',3)
    cv2.namedWindow('Color', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Color', 470,0)
    cv2.resizeWindow('Color', 46,150)
    # Display an image
    cv2.imshow('Color',img)
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
