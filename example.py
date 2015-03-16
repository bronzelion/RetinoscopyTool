from OpenGL.GL import *
from OpenGL.GLUT import *
from PyQt4 import *
from PyQt4.QtOpenGL import *
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import QColor,QPixmap,QLabel
import math,os, PIL.Image
import numpy as np


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.eye_power = 4
       
        self.GLWidget = WfWidget()
        '''self.slider =QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider.setGeometry(30, 40, 100, 30)
        self.slider.setMinimum(-10)
        self.slider.setMaximum(10)
        self.slider.valueChanged[int].connect(self.changeValue)'''
        #pic = QtGui.QLabel()
        #pic.setGeometry(10, 10, 400, 200)
        #pixmap = QtGui.QPixmap("eye2.jpg")
        #pixmap = pixmap.scaledToHeight(200)
        #pic.setPixmap(pixmap)

        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.GLWidget)
        #mainLayout.addWidget(pic)
        self.setLayout(mainLayout)
        

    def changeValue(self,value):
        self.GLWidget.diff = self.eye_power - value
        print 'Difference' , self.GLWidget.diff
        self.GLWidget.updateGL()
        
class WfWidget(QGLWidget):
    def __init__(self, parent = None):
        super(WfWidget, self).__init__(parent)
        self.diff =2
        self.setMouseTracking(True)
        
        self.mx = 0
        self.my =0
              

        self.pixmap = QtGui.QPixmap("eye1.jpg")
        #self.pixmap = self.pixmap.scaledToHeight(500)
        
        #self.bindTexture(self.pixmap,GL_TEXTURE_2D,GL_RGBA)
        #self.texture = []
        #self.textureMap()

        #self.MainTex = glGenTextures(1)
        #self.TexFromPNG("eye2.jpg")
        
    
    def drawCircle(self,cx, cy, r, num_segments) :
        #print 'In draw'
        #print 'CX CY',cx,cy
        self.drawLowerCircle(cx, cy, r, num_segments)

    

    def drawLowerCircle(self,cx, cy, r, num_segments):
        
        vlist=[]
        
        for ii in range(num_segments):
           
            theta = 2.0 * 3.1415926 * (ii) / (num_segments)
            x = r * math.cos(theta);
            y = r * math.sin(theta);
            vlist.append((cx+x,cy+y))
        #print vlist
        
        polyLista=[]
        polyListb =[]
        step = (4 - self.diff)
        for i in range(step):
            mid = 8
            polyLista.append(mid-i)
            polyListb.append(mid+i)
            
        tempa = list(polyLista)
        tempb = list(polyListb)
        for i in range(1,step+1):
            polyLista.append(mid - tempa[-i])

        print 'Step = ', step
        for i in range(step,0,-1):
            count =17
            #print 'aPP', step
            polyListb.append((count-i) %16)
        
        print polyLista,polyListb
        self.drawPoly(polyLista,vlist)
        self.drawPoly(polyListb,vlist)
        glFlush();
        
    def drawPoly(self,polyList,vlist):
        glBegin(GL_POLYGON);
        for i in polyList:
            #if i == 0 or i == 8:
            glColor3f(1.0, 0.5, 0.0)
            #else:
                #glColor3f(0.0, 0.0, 0.0)
            glVertex2f(vlist[i][0],vlist[i][1])
        glEnd();
        
            
        
        '''  for ii in range(num_segments):
            #if ii <8:
            #    glColor3f(0.0, 1.0, 1.0)
            #else:
            
            theta = 2.0 * 3.1415926 * (ii) / (num_segments)
            x = r * math.cos(theta);
            y = r * math.sin(theta);
            
            if(ii <= 1+(4-self.diff)  or (ii >= 7- (4-self.diff) and ii <=9+(4- self.diff)) or (ii>12+(4-self.diff) and ii <= 15)):
                if (ii ==0 or ii ==8 ):
                    glColor3f(1.0, 0.5, 0.0)
                     
                else:
                     glColor3f(0.0, 0.0, 0.0)
                print 'IDX',ii
                glVertex2f(x + cx, y + cy);
        glEnd();
        glglFlush();();'''
 
    def mouseMoveEvent(self,event):
        #print 'In Mouse Move'
        self.mx = event.x()
        self.my = self.height()-event.y()
        print self.mx,self.my
        #self.drawCircle(x,y,10,16)
        #self.swapBuffers()
        self.updateGL()
        #print self.doubleBuffer()
        

   
    
    def paintGL(self):
      
        glClearColor(0,0,0,0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT| GL_STENCIL_BUFFER_BIT);

        
        
        #glMatrixMode( GL_PROJECTION );
        #glLoadIdentity();
        #glOrtho(0, 500, 0, 500, -500.0, 500.0)
        glEnable(GL_DEPTH_TEST);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        
        glTranslatef(0,0,-200)
        glRotatef(-90,0,0,1)
        glColor3f(1,1,1)
        self.texid =self.bindTexture(self.pixmap,GL_TEXTURE_2D,GL_RGBA)
        #r = QtCore.QRectF(500.0,500.0,0.0,0.0)
        r = QtCore.QRectF(QtCore.QPoint(0,self.width()),QtCore.QPoint(self.width(),0))
        print r.topLeft(), r.bottomRight()
        glRotatef(90,0,0,1)
        self.drawTexture(r,self.texid,GL_TEXTURE_2D)
        
        glTranslatef(0,0,200)

        #glBindTexture(GL_TEXTURE_2D, self.SplashTex)
        #glColorf(1,1,0)
	#glPoint(100,400)
        glPolygonMode (GL_FRONT_AND_BACK,GL_FILL )
        '''glClearColor(0.0, 0.0, 0.0, 0.1);
        glColor3f(1,0,0)
        glRectf(self.mx-30, self.my-10, self.mx+30, self.my+10)'''
        self.cursorRectangle(self.mx-130, self.my-5, self.mx+50, self.my+5)
        #if self.mx >=225 and self.mx <= 275 and self.my>=225 and self.my <= 275:
        if self.mx >=130 and self.mx <= 260 and self.my>=160 and self.my <= 310:
            self.drawCircle(self.mx ,self.my ,50,16)


    def resizeGL(self, width, height):
        print 'wh', width, height

        side = min(width, height)
        if side < 0:
            return

       
        glViewport(0,0,width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -500.0, 500.0)
        #glViewport((width - side) // 2, (height - side) // 2, side, side)
        
        #GL.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        glMatrixMode(GL_MODELVIEW)
        self.setGeometry(0,0,width,height)
        self.updateGL()
        
        '''glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        glViewport(0, 0, w, h)'''

    def initializeGL(self):
        print 'INIT'
        #print self.width(), self.height()
        #glClearColor(0.0, 0.0, 0.0, 1.0)
        
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT| GL_STENCIL_BUFFER_BIT);
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA|GLUT_DEPTH)
        
        
    def maximumSize(self):        
        return QtCore.QSize(500, 500)
    def sizeHint(self):
        return QtCore.QSize(500, 500)

    def cursorRectangle(self,x1,y1,x2,y2):
        
        #glClearColor(0,0,0,0.5)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT| GL_STENCIL_BUFFER_BIT);
       
        glColor3f(1.0,1.0,1.0)
        glBegin(GL_POLYGON);
        glVertex2f( x1, y1 );
        glVertex2f( x2, y1 );
        glColor3f(0.0,0.0,0.0)
        glVertex2f( x2, y2 );
        glVertex2f( x1, y2 );
        glEnd();
        glFlush();
           

if __name__ == '__main__':
    app = QtGui.QApplication(["Winfred's PyQt OpenGL"])
    widget = Window()
    widget.show()
    app.exec_()
