#!/usr/bin/python
# -*- coding: UTF-8 -*-
import n5110,time,threading

class Banner(threading.Thread):
	
	def __init__(self,msg="Hola mundo"):
		threading.Thread.__init__(self)
		self.msg=msg
		self.running=False
		self.screen=n5110.Screen()
		self.screen.lcdInitialise()
		self.screen.clear()
		self.tp=5
		self.cps=84
		self.cline=14

	def backLight(self,on):
		self.screen.lcdBacklight(on)

	def showMessage(self,msg):
		fin=False
		while not fin:
			try:
				i=msg.index('\n')
				n=self.cline-i%self.cline
				msg=msg[:i]+" "*n+msg[i+1:]
			except:
				fin=True
		tl=len(msg)
		ts=1+tl/self.cps
		for i in range(ts):
			self.screen.clear()
			self.screen.draw()
			ss=msg[i*self.cps:self.cps*(i+1)]
			self.screen.drawString(0,0,ss)
			self.screen.draw()
			time.sleep(self.tp)
	
	def run(self):
		self.running=True
		while self.running:
			self.showMessage(self.msg)

	def setMsg(self,msg):
		self.msg=msg.strip()

	def stop(self):
		self.running=False
if __name__=="__main__":
	m=Banner()
	m.start() 
	quit=False
	while not quit:
		msg=raw_input()
		if msg=='q':
			m.stop()
			quit=True
		else:
			m.setMsg(msg)

