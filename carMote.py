#!/usr/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'carMote.ui'
#
# Created: Sun Sep  1 23:22:03 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

import time,datetime,threading,thread,socket,select

class CarMoteConnection(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running=False
		self.vel=0
		self.turn=0
		self.lastSend=None
	def setVel(self,vel):
		self.vel=vel
	def setTurn(self,turn):
		self.turn=turn
	def init(self):
		self.running=True
		self.start()
	def stop(self):
		self.running=False
	def run(self):
		BUFF = 20
		HOST = '192.168.1.12'
		PORT = 3434
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		while self.running:
			message=str(self.vel)+","+str(self.turn)
			if message!="0,0" or self.lastSend!=message:
				print "sending ",message
				s.send(message)
				data = s.recv(BUFF)
				print data
				self.lastSend=message
			
			time.sleep(0.1)
		s.close()

from PyQt4 import QtCore, QtGui

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

class Ui_Frame(QtGui.QFrame):
	def __init__(self):
		QtGui.QFrame.__init__(self)
	def setupUi(self, Frame,server):
		self.server=server
		Frame.setObjectName(_fromUtf8("Frame"))
		Frame.resize(400, 140)
		Frame.setFrameShape(QtGui.QFrame.StyledPanel)
		Frame.setFrameShadow(QtGui.QFrame.Raised)
		self.btnLeft = QtGui.QPushButton(Frame)
		self.btnLeft.setGeometry(QtCore.QRect(240, 40, 61, 51))
		self.btnLeft.setObjectName(_fromUtf8("btnLeft"))
		self.btnForward = QtGui.QPushButton(Frame)
		self.btnForward.setGeometry(QtCore.QRect(30, 20, 61, 51))
		self.btnForward.setObjectName(_fromUtf8("btnForward"))
		self.btnBackwards = QtGui.QPushButton(Frame)
		self.btnBackwards.setGeometry(QtCore.QRect(30, 70, 61, 51))
		self.btnBackwards.setObjectName(_fromUtf8("btnBackwards"))
		self.btnRight = QtGui.QPushButton(Frame)
		self.btnRight.setGeometry(QtCore.QRect(300, 40, 61, 51))
		self.btnRight.setObjectName(_fromUtf8("btnRight"))

		self.retranslateUi(Frame)
		QtCore.QMetaObject.connectSlotsByName(Frame)
	
		QtCore.QObject.connect(self.btnForward,QtCore.SIGNAL("pressed()"),self.btnForwardAction)
		QtCore.QObject.connect(self.btnForward,QtCore.SIGNAL("released()"),self.clearVelAction)
		QtCore.QObject.connect(self.btnBackwards,QtCore.SIGNAL("pressed()"),self.btnBackwardAction)
		QtCore.QObject.connect(self.btnBackwards,QtCore.SIGNAL("released()"),self.clearVelAction)

		QtCore.QObject.connect(self.btnRight,QtCore.SIGNAL("pressed()"),self.btnRightAction)
		QtCore.QObject.connect(self.btnRight,QtCore.SIGNAL("released()"),self.clearTurnAction)
		QtCore.QObject.connect(self.btnLeft,QtCore.SIGNAL("pressed()"),self.btnLeftAction)
		QtCore.QObject.connect(self.btnLeft,QtCore.SIGNAL("released()"),self.clearTurnAction)
	
	def keyPressEvent(self,event):
		k=event.text()
		if k=="w":
			self.btnForwardAction()
			print "FW!"
		elif k=="x":
			self.btnBackwardAction()
		elif k=="a": 
			self.btnLeftAction()
		elif k=="d":
			self.btnRightAction()
	
	def keyReleaseEvent(self,event):
		k=event.text()
		if k=="w" or k=="x":
			self.clearVelAction()
		elif k=="a" or k=="d":
			self.clearTurnAction()

	def btnForwardAction(self):
		self.server.setVel(1)
	def btnBackwardAction(self):
		self.server.setVel(-1)
	def btnRightAction(self):
		self.server.setTurn(1)
	def btnLeftAction(self):
		self.server.setTurn(-1)
	def clearVelAction(self):
		self.server.setVel(0)
	def clearTurnAction(self):
		self.server.setTurn(0)
	
	def move(self,f,t):
		self.server.setMessage(f+","+t)
	def exit(self):
		self.server.stop()

	def retranslateUi(self, Frame):
		Frame.setWindowTitle(_translate("Frame", "CarMote", None))
		self.btnLeft.setText(_translate("Frame", "<", None))
		self.btnForward.setText(_translate("Frame", "^", None))
		self.btnBackwards.setText(_translate("Frame", "v", None))
		self.btnRight.setText(_translate("Frame", ">", None))

if __name__ == "__main__":
	import sys
	connection=CarMoteConnection()
	connection.init()
	app = QtGui.QApplication(sys.argv)
	Frame = Ui_Frame()
	Frame.setupUi(Frame,connection)
	Frame.show()
	QtCore.QObject.connect(app,QtCore.SIGNAL("aboutToQuit()"),Frame.exit)
	sys.exit(app.exec_())
