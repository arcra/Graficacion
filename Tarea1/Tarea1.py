#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from random import Random

'''Ejemplo basado en un artículo en la siguiente liga: http://zetcode.com/tutorials/pyqt4/drawing/'''

class PaintWindow(QWidget):
	
	def __init__(self):
		
		super(PaintWindow, self).__init__()
		
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle('Tarea1 - Adrian Revuelta Cuauhtli')
		self.setGeometry(100, 200, 600, 400)
		self.show()
		
	def paintEvent(self, e):
		qpainter = QPainter()
	
		qpainter.begin(self)
		
		#Draw background
		qpainter.setBrush(Qt.black)
		qpainter.drawRect(QRect(0, 0, 600, 400))
		
		#Draw dots
		qpainter.setPen(Qt.white)
		r = Random()
		for x in range(100):
			qpainter.drawPoint(r.randint(1, self.width()), r.randint(1,self.height()))
		
		
		qpainter.end()

if __name__ == '__main__':

	app = QApplication(sys.argv)
	
	mainWindow = PaintWindow()
	
	sys.exit(app.exec_())