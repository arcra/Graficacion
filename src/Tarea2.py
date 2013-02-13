#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QWidget, QPainter, QApplication
from PyQt4.QtCore import Qt, QRect
from math import sin, cos, pi

def multiplyMatrix(M1, M2):
	M3 = []
	for row in xrange(len(M1)):
		M3.append([])
		for column in xrange(len(M2[0])):
			value = 0
			for m in xrange(len(M1[0])):
				value += M1[row][m]*M2[m][column]
			M3[row].append(value)
	return M3

def getRotationMatrix(angle):
	angle = -angle*pi/180
	sinx = sin(angle)
	cosx = cos(angle)
	return [[cosx,	-sinx,	0],
			[sinx,	cosx,	0],
			[0,		0,		1]]


class arcPoint():
	
	def __init__(self, x, y, color=Qt.white):
		self.x = x
		self.y = y
		self.color = color
	
	def translate(self, dx, dy):
		self.x = self.x + dx
		self.y = self.y + dy
	
	def rotate(self, angle):
		rotationMatrix = getRotationMatrix(angle)
		rotatedPoint = multiplyMatrix(rotationMatrix, [[self.x], [self.y], [1]])
		self.x = int(rotatedPoint[0][0])
		self.y = int(rotatedPoint[1][0])

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
			#To make points bigger, draw 9 pixel stencil around that point
			for dx in range(-1,2):
				for dy in range(-1,2):
					qpainter.drawPoint(p.x + dx, p.y + dy)
		
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

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	#originalImageWindow
	orImg = arcCanvasWindow('Tarea2 - Original - Adrian Revuelta Cuauhtli')
	rotatedImg = arcCanvasWindow('Tarea2 - Rotada(30) - Adrian Revuelta Cuauhtli')
	
	halfWidth = orImg.width()//2
	
	triangle = [arcPoint(halfWidth, 50), arcPoint(halfWidth-50, 100), arcPoint(halfWidth+50, 100)]
	
	
	for p in triangle:
		orImg.addPoint(p)
		newPoint = arcPoint(p.x, p.y)
		newPoint.translate(-halfWidth, -75)
		newPoint.rotate(30)
		newPoint.translate(halfWidth, 75)
		rotatedImg.addPoint(newPoint)
	
	sys.exit(app.exec_())