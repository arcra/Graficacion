#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QWidget, QPainter, QApplication
from PyQt4.QtCore import Qt, QRect
from copy import deepcopy


class arcPolygon():
	
	def __init__(self, points=None):
		if points is None:
			self.points = []
		else:
			self.points = deepcopy(points)
	
class arcPoint():
	
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color

class arcCanvasWindow(QWidget):
	
	def __init__(self, title='New Canvas Window', width=600, height=400, x=100, y=200):
		
		super(arcCanvasWindow, self).__init__()
		
		self.backgroundBrush = Qt.black
		self.points = set([])
		
		self.initUI(title, width, height, x, y)
	
	def initUI(self, title, width, height, x, y):
		self.setWindowTitle(title)
		self.setGeometry(x, y, width, height)
		self.show()
		
	def paintEvent(self, e):
		qpainter = QPainter()
	
		qpainter.begin(self)
		
		#Draw background
		qpainter.setBrush(self.backgroundBrush)
		qpainter.drawRect(QRect(0, 0, self.width(), self.height()))
		
		for p in self.points:
			qpainter.setPen(p.color)
			qpainter.drawPoint(p)
		
		qpainter.end()
	
	def setBackgroundBrush(self, color):
		'''Sets the background color to the specified QBrush
			Keyword arguments:
			    color -- the QBrush or QColor to be used to paint the background
		'''
		self.backgroundBrush = color
	
	def addPoint(self, point):
		'''Adds a point to be drawn in this canvas
			Keyword arguments:
				point -- an arcPoint to be drawn in this canvas 
		'''
		self.points.add(point)
	
	def addPolygon(self, polygon):
		'''Adds a polygon to be drawn in this canvas
			Keyword arguments:
				polygon -- an arcPolygon to be drawn in this canvas 
		'''

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	mainWindow = arcCanvasWindow('Tarea2 - Adrian Revuelta Cuauhtli')
	
	sys.exit(app.exec_())