from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *    
from db import *
from connect import DBconnect
from pynput.keyboard import Key, Controller
import numpy as np
import pymysql
import csv
import sys

connection = DBconnect()
allrally = GetAllRally(connection)
loserally = GetLoseRally(connection,'B')
data = GetRallyPosition(connection,allrally[0][0],allrally[0][1])
btype = GetRallyType(connection,allrally[0][0],allrally[0][1])
arrlen = data.size  
rallyc =0
rallyl = -1
idc = 0

def init():
    glClearColor(1,1,1,1)
    gluOrtho2D(400,0,0,850)   #left, right, bottom, top
    
def line():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # glColor3f(1,0,0)

    # posx, posy = 0,0    
    # sides = 32    
    # radius = 1    
    # glBegin(GL_POLYGON)    
    # for i in range(100):    
    #     cosine= radius * cos(i*2*pi/sides) + posx    
    #     sine  = radius * sin(i*2*pi/sides) + posy    
    #     angle = 2 * pi / sides
    #     x = 100
    #     y = 200

    #     glVertex2f(x,y)

    # glEnd()
    # glFlush()

    glLineWidth(5)
    glBegin(GL_LINES)
    # glBegin(GL_LINE_STRIP)
    glColor3f(1,0,0)
    # glColor3f(0.9804,0.502,0.4471)
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

    # glVertex2f(25.0,25.0)
    # glVertex2f(50.0,25.0)
    
    # glVertex2f(50.0,50.0)
    #  glColor3f(1,0,0)
    # glVertex2f(-1, -1)
    
    # glColor3f(0,1,0)
    # glVertex2f(1, -1)
    
    # glColor3f(0,0,1)
    # glVertex2f(0, 1)
    
    glEnd()
    glFlush()

    glLineWidth(2)
    glBegin(GL_LINES)

    var=0.95

    for i in range(len(data)-1):
        x1,y1 = data[i]
        x2,y2 = data[i+1]
        midx = (x2+x1)/2.0 
        midy = (y1+y2)/2.0 
        
        var=var - 1.0/data.size
        glColor3f(0,1-var,1-var)
        
        glVertex2f(x1,y1)
        glVertex2f(midx,midy)
        
        var=var - 1.0/data.size
        glColor3f(0,1-var,1-var)
        
        glVertex2f(midx,midy)
        glVertex2f(x2,y2)

    glEnd()
    glFlush()

    glPointSize(20)
    glBegin(GL_POINTS)
    glColor3f(0,0,0)
    glVertex2f(data[0][0],data[0][1])
    glEnd()
    glFlush()

    glPointSize(15)
    glBegin(GL_POINTS)
    glColor3f(0,0,1)

    # print(btype.shape)
    # print(btype)
    for i in range(data.shape[0]-1):
        # if i == 0:
        #     glColor3f(0.9804,0.502,0.4471)
        # if i == data.shape[0]-1:
        #     glColor3f(0.804,0.2,0.2)
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
        glColor3f(0,0,1)
    glEnd()
    glFlush()


    glPointSize(20)
    glBegin(GL_POINTS)
    glColor3f(0,1,1)
    glVertex2f(data[data.shape[0]-1][0],data[data.shape[0]-1][1])
    glEnd()
    glFlush()

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

    if key == 'a':
        if rallyc==0:
            print("There's no previous rally!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        rallyc=rallyc-1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print(data)
        print(btype)
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        line()

    if key == 'd':
        if rallyc>=len(allrally)-1:
            print("There's no next rally!")
            print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
            return
        rallyc=rallyc+1
        data = GetRallyPosition(connection,allrally[rallyc][0],allrally[rallyc][1])
        btype = GetRallyType(connection,allrally[rallyc][0],allrally[rallyc][1])
        print('Here is game:', allrally[rallyc][0], ', rally:', allrally[rallyc][1])
        line()

    if key == 'w':
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
        line()

    if key == 's':
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
        line()
    
    if key == 'h':
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
        line()
    if key == 'f':
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
        line()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(400,850) #height,width glutInitWindowSize(400,850)
    glutInitWindowPosition(50,50)
    glutCreateWindow("Course")

    glEnable(GL_POINT_SMOOTH)
    glutDisplayFunc(line)
    glRotatef(180.0, 0.0, 0.0, 1.0)
    init()
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == '__main__':
    main()


# from OpenGL.GL import *
# #import OpenGL as gl

# glClearColor(1.0, 1.0, 1.0, 0.0)
# glClear(GL_COLOR_BUFFER_BIT)
# glBegin(GL_TRIANGLES)
# glColor3f(1.0,0.0,0.0)
# glVertex2f(50.,50.)
# glVertex2f(150.,50.)
# glVertex2f(100.,150.)

# glEnd()

# glFlush()