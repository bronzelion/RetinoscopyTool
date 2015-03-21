# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\UI\temp.ui'
#
# Created: Tue Mar 10 23:05:50 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

'''
Author : Harsha.K.C

Usage: Retinoscopytool.py [power of the eye to be set, default is +4]

Desc :
This tool is an attempt to explain the concept of Retinoscopy and how
ophthalmologists could learn by this experiment before treating a patient.
The power of the eye if not specified is assumed to be +4.

This tool gives a way to identify/estimate the power of the eye. When
power of the eye matches the lens used to shine light, that can be seen by
a complete circular light beam.

Try playing around with different powers to get a hang of the concept.
Inbox harshakc01@gmail.com regarding any sort of queries tool

Cheers!
'''


from PyQt4 import QtCore, QtGui
from Retinolib import *
import sys
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
       
        super(Ui_Form,self).__init__()
        QtGui.QWidget.__init__(self)
        self.GLWidget = Window()
        self.setupUi(self)
        
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Retinoscopy Tool"))
        Form.resize(500, 500)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        #self.widget = QtGui.QWidget(Form)
        #self.widget.setObjectName(_fromUtf8("widget"))
        self.widget = self.GLWidget
        self.verticalLayout.addWidget(self.widget)
        spacerItem = QtGui.QSpacerItem(20, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalSlider = QtGui.QSlider(Form)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalSlider.setMinimum(-10)
        self.horizontalSlider.setMaximum(10)
        self.GLWidget.slider_val = self.horizontalSlider.value()

        self.label = QtGui.QLabel("Lens Power : 0")
        self.verticalLayout.addWidget(self.label)
        
        
        self.retranslateUi(Form)
        #QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.compute)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.GLWidget.changeValue)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelVal)
        
        QtCore.QMetaObject.connectSlotsByName(Form)

    def labelVal(self,val):
        self.label.setText(self.label.text().split(':')[0]+ ': '+str(val))
        #print diff

    def sizeHint(self):
        return QtCore.QSize(500, 700)
    def maximumSize(self):        
        return QtCore.QSize(500, 700)
    

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.setMouseTracking(True);
    ex.show()
    sys.exit(app.exec_())

