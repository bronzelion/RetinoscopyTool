from OpenGL.GL import *
from OpenGL.GLUT import *
from PyQt4 import *
from PyQt4.QtOpenGL import *
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import QColor,QPixmap,QLabel
import math,os,sys


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        if len(sys.argv) ==2:
            self.eye_power = int(sys.argv[1])
        else:
            self.eye_power = 4
       
        self.GLWidget = WfWidget()
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.GLWidget)
        #mainLayout.addWidget(pic)
        self.setLayout(mainLayout)
        

    def changeValue(self,value):
        self.GLWidget.diff = self.eye_power - value
        #print 'Difference updates' , self.GLWidget.diff
        self.GLWidget.eye_proxy = self.eye_power
        self.GLWidget.updateGL()
        
class WfWidget(QGLWidget):
    def __init__(self, parent = None):
        super(WfWidget, self).__init__(parent)
        self.diff =5
        self.setMouseTracking(True)
        self.vertexList=[]
        self.mx = 0
        self.my =0
        self.eye_proxy=0
        self.up = True
        self.move =20
        self.pixmap = QtGui.QPixmap("eye2.jpg")
        #self.computeVertices(0,0,)
        self.top,self.bottom = self.polyList(32)

       
    def polyList(self,segments):
        half = segments/2
        fourth = segments/ 4
        last = segments -1

        inc =[0,1,3,6,fourth]
        inc = fourth
        polyTop=[]
        polyDown=[]
        #for i in inc:
        for i in range(fourth):
            level =i
            polyTop.insert(0,[level,half-level,half-1-level,level+1])
            polyDown.insert(0,[0 if i==0 else (last-level+1),half+level,half+1+level,last if i ==0 else last-level])

        #print 'Top', polyTop
        #print 'Bottom',polyDown

        return polyTop,polyDown

    def computeVertices(self,cx, cy, r, num_segments):
        self.vertexList =[]
        for ii in range(num_segments):
           
            theta = 2.0 * 3.1415926 * (ii) / (num_segments)
            x = r * math.cos(theta);
            y = r * math.sin(theta);
            self.vertexList.append((cx+x,cy+y))
            
        #print 'VList len',len(self.vertexList)
    
    def drawCircle(self,cx, cy, r, num_segments) :
        
        self.computeVertices(cx,cy,r,num_segments)
        #self.polyList(num_segments)
        #print 'Diff', self.diff
        #print 'Prod ',self.diff * self.eye_proxy 
        
        if abs(self.diff) >=4:
            self.drawLight(6)
        elif abs(self.diff) in [3]:
            self.drawLight(5)
        elif abs(self.diff) in [2]:
            self.drawLight(4)
        else:
            self.drawLight(abs(self.diff))

    
    def drawLight(self,idx):
        #print "vlist range", range(idx,8)
        glClearColor(0,0,0,0)
        for i in range(idx,8):            
            top = self.top[i]
            glColor3f(1.0, 0.5, 0.0)
            glBegin(GL_POLYGON)
            for j in top:
                if (idx == i or idx == i+1)and (j in top[2:]):
                    glColor3f(0,0,0)
                elif (i>=4 and i<=5)and (j in top[2:]):
                    glColor3f(1.05,0.55,0)
                
                glVertex3f(self.vertexList[j][0],self.vertexList[j][1],0)
            glEnd()

            bot = self.bottom[i]
            glColor3f(1.0, 0.5, 0.0)
            glBegin(GL_POLYGON)
            for j in bot:
                if idx == i and (j == bot[2]):
                    glColor3f(0,0,0)    
                glVertex3f(self.vertexList[j][0],self.vertexList[j][1],0)
            glEnd()
        #glFlush()  

    def mouseMoveEvent(self,event):
        
        self.mx = event.x()
        self.my = self.height()-event.y()
        #print self.mx,self.my       
        self.updateGL() 
    
    def paintGL(self):
      
        glClearColor(0,0,0,0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT| GL_STENCIL_BUFFER_BIT);

        glEnable(GL_DEPTH_TEST);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        
        glTranslatef(0,0,-200)
        glRotatef(-90,0,0,1)
        glEnable(GL_BLEND)
        glColor4f(1,1,1,0.6)
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        self.texid =self.bindTexture(self.pixmap,GL_TEXTURE_2D,GL_RGBA)
        #r = QtCore.QRectF(500.0,500.0,0.0,0.0)
        r = QtCore.QRectF(QtCore.QPoint(0,self.width()),QtCore.QPoint(self.width(),0))
        #print r.topLeft(), r.bottomRight()
        glRotatef(90,0,0,1)
        self.drawTexture(r,self.texid,GL_TEXTURE_2D)
        glColor4f(1,1,1,1)
        glTranslatef(0,0,200)
        
        glPolygonMode (GL_FRONT_AND_BACK,GL_FILL )
        
        self.cursorRectangle(self.mx-130, self.my-5, self.mx+50, self.my+5)
        #if self.mx >=225 and self.mx <= 275 and self.my>=225 and self.my <= 275:

        if self.mx >=180 and self.mx <= 230 and self.my>=200 and self.my <= 280:
            if not self.diff * self.eye_proxy >=0 and self.move >= -40 and self.move <=40:
                self.move = self.my - 240
                self.drawCircle(self.mx,240 -self.move ,40,32)
                
            else:
                #self.move =20
                self.drawCircle(self.mx ,self.my ,40,32)
        #else:
        #   self.move =20

    def resizeGL(self, width, height):
        #print 'wh', width, height
        side = min(width, height)
        if side < 0:
            return
        glViewport(0,0,width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -500.0, 500.0)
        glMatrixMode(GL_MODELVIEW)
        self.setGeometry(0,0,width,height)
        self.updateGL()

    def initializeGL(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA|GLUT_DEPTH)
                
    def maximumSize(self):        
        return QtCore.QSize(500, 500)
    def sizeHint(self):
        return QtCore.QSize(500, 500)

    def cursorRectangle(self,x1,y1,x2,y2):
        
        glColor4f(1.0,1.0,1.0,0.3)
        glBegin(GL_POLYGON);
        glVertex3f( x1, y1,-10 );
        glVertex3f( x2, y1,-10 );
        glColor4f(0.0,0.0,0.0,0.3)
        glVertex3f( x2, y2 ,-10);
        glVertex3f( x1, y2 ,-10);
        glEnd();
        glFlush();
           

if __name__ == '__main__':
    app = QtGui.QApplication(["Winfred's PyQt OpenGL"])
    widget = Window()
    widget.show()
    app.exec_()
