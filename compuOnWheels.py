#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time,datetime,threading,thread,socket,select
PIN_FORWARD="P8_11"
PIN_BACKWARD="P8_12"
PIN_LEFT="P8_15"
PIN_RIGHT="P8_16"

class Car(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.velocity=0
		self.actualVelocity=0
		#positive right
		self.turn=0
		self.actualTurn=0
		self.lastCommand=datetime.datetime.now()
		self.running=True
	def init(self):
		GPIO.setup(PIN_FORWARD, GPIO.OUT)
		GPIO.setup(PIN_BACKWARD, GPIO.OUT)
		GPIO.setup(PIN_LEFT, GPIO.OUT)
		GPIO.setup(PIN_RIGHT, GPIO.OUT)
		self.start()
	def updateTime(self):
		self.lastCommand=datetime.datetime.now()
	def goForward(self):
		self.go(1,self.turn)
	def goBackwards(self):
		self.go(-1,self.turn)
	def goRight(self):
		self.go(self.vel,1)
	def goLeft(self):
		self.go(self.vel,-1)
	def go(self,vel,turn):
		self.velocity=vel
		self.turn=turn
		self.updateTime()
	def move(self):
		vel=self.velocity
		if self.actualVelocity>=0 and vel<0:
			GPIO.output(PIN_FORWARD,GPIO.LOW)
			GPIO.output(PIN_BACKWARD,GPIO.HIGH)
		elif self.actualVelocity<=0 and vel>0:
			print "Go forward!"
			GPIO.output(PIN_BACKWARD,GPIO.LOW)
			GPIO.output(PIN_FORWARD,GPIO.HIGH)
		elif vel==0:
			GPIO.output(PIN_FORWARD,GPIO.LOW)
			GPIO.output(PIN_BACKWARD,GPIO.LOW)
		self.actualVelocity=vel
		t=self.turn
		if self.actualTurn>=0 and t<0:
			GPIO.output(PIN_RIGHT,GPIO.LOW)
			GPIO.output(PIN_LEFT,GPIO.HIGH)
		elif self.actualTurn<=0 and t>0:
			GPIO.output(PIN_LEFT,GPIO.LOW)
			GPIO.output(PIN_RIGHT,GPIO.HIGH)
		elif t==0:
			GPIO.output(PIN_LEFT,GPIO.LOW)
			GPIO.output(PIN_RIGHT,GPIO.LOW)
		self.actualTurn=t

	def stop(self):
		self.running=False
		GPIO.cleanup()
	def run(self):
		while self.running:
			t=datetime.datetime.now()-self.lastCommand
			print "msecs ",t.total_seconds()
			if t.total_seconds()>0.5:
				self.velocity=0
				self.turn=0
				print "Wiping"
			self.move()
			time.sleep(0.25)

class CarServer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running=False
		self.car=Car()
	def init(self):
		self.running=True
		self.car.init()
		self.start()
	def stop(self):
		self.car.stop()
		self.running=False
	def run(self):
		BUFF = 20
		HOST = '192.168.1.12'
		PORT = 3434
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((HOST, PORT))
		server_socket.listen(5)
		print "Listening on port ",PORT
		read_list = [server_socket]
		while self.running:
			readable, writable, errored = select.select(read_list, [], [],5)
			print readable
			for s in readable:
				if s is server_socket:
					client_socket, address = server_socket.accept()
					read_list.append(client_socket)
					print "Connection from", address
				else:
					data = s.recv(BUFF)
					try:
						dat=data.split(",")
						if len(dat)!=2:
							raise Exception("Bad format")
						f=int(dat[0])
						t=int(dat[1])
						self.car.go(f,t)
					except:
						data="Sytax: [num],[num]\n"
					if data:
						try:
							s.send(data)
						except:
							data=None
					if data==None:
						try:
							s.close()
						except:
							pass
						read_list.remove(s)
		server_socket.close()
if __name__=='__main__':
	server=CarServer()
	server.init()
	r=raw_input()
	while r!='q':
		r=raw_input()
	server.stop()
