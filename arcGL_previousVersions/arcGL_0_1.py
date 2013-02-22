#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QWidget, QPainter, QApplication
from PyQt4.QtCore import Qt, QRect, SIGNAL
from math import sin, cos, pi, sqrt

matrixStack = []
currentMatrix = [	[1, 0, 0, 0],
					[0, 1, 0, 0],
					[0, 0, 1, 0],
					[0, 0, 0, 1]
				]

points = []
tempPoints = []

def arcSetPoint(p):
	global tempPoints, points
	if len(matrixStack) == 0:
		newPoint = arcMultiplyMatrices(currentMatrix, [[p.x], [p.y], [p.z], [1]])
		p.x = newPoint[0][0]
		p.y = newPoint[1][0]
		p.z = newPoint[2][0]
		points.append(p)
	else:
		tempPoints[-1].append(p)

def arcPushMatrix():
	global matrixStack, tempPoints
	matrixStack.append(currentMatrix)
	tempPoints.append([])

def arcPopMatrix():
	global matrixStack, tempPoints, points, currentMatrix
	tmp = tempPoints.pop()
	for p in tmp:
		newPoint = arcMultiplyMatrices(currentMatrix, [[p.x], [p.y], [p.z], [1]])
		p.x = newPoint[0][0]
		p.y = newPoint[1][0]
		p.z = newPoint[2][0]
		points.append(p)
	currentMatrix = matrixStack.pop()

def arcTranslate(dx, dy, dz):
	global currentMatrix
	translationMatrix = [
						[1, 0, 0, dx],
						[0, 1, 0, dy],
						[0, 0, 1, dz],
						[0, 0, 0, 1],
						]
	
	currentMatrix = arcMultiplyMatrices(currentMatrix, translationMatrix)

def arcScale(sx, sy, sz):
	global currentMatrix
	scalationMatrix = [
						[sx, 0, 0, 0],
						[0, sy, 0, 0],
						[0, 0, sz, 0],
						[0, 0, 0, 1],
						]
	
	currentMatrix = arcMultiplyMatrices(currentMatrix, scalationMatrix)

def arcRotateX(angle):
	global currentMatrix
	angle = angle*pi/180
	sinx = sin(angle)
	cosx = cos(angle)
	
	rotationX = [
				[1,		0, 		0,		0],
				[0,		cosx,	sinx,	0],
				[0,		-sinx,	cosx,	0],
				[0,		0, 		0,		1]
				]
	
	currentMatrix = arcMultiplyMatrices(currentMatrix, rotationX)

def arcRotateY(angle):
	global currentMatrix
	
	angle = angle*pi/180
	
	siny = sin(angle)
	cosy = cos(angle)
	
	rotationY = [
				[cosy,	0, 		siny,	0],
				[0,		1,		0,		0],
				[-siny,	0,		cosy,	0],
				[0,		0, 		0,		1]
				]
	
	currentMatrix = arcMultiplyMatrices(currentMatrix, rotationY)
	
def arcRotateZ(angle):
	global currentMatrix
	angle = angle*pi/180
	
	sinz = sin(angle)
	cosz = cos(angle)
	
	rotationZ = [
				[cosz,	sinz, 	0,	0],
				[-sinz,	cosz,	0,	0],
				[0,		0,		1,	0],
				[0,		0, 		0,	1]
				]
	
	currentMatrix = arcMultiplyMatrices(currentMatrix, rotationZ)

def arcMultiplyMatrices(*matrices):
	M = matrices[0]
	for index in range(len(matrices) - 1):
		tempM = []
		for row in range(len(M)):
			tempM.append([])
			for column in range(len(matrices[index+1][0])):
				value = 0
				for m in range(len(M[0])):
					value += M[row][m]*matrices[index+1][m][column]
				tempM[row].append(value)
		M = tempM
	return M

def arcNormalize(p):
	norm = sqrt(p.x*p.x + p.y*p.y + p.z*p.z)
	if norm > 0:
		p.x = p.x/norm
		p.y = p.y/norm
		p.z = p.z/norm
	
	return p

class arcPoint():
	
	def __init__(self, x, y, z=0, color=Qt.white):
		self.x = x
		self.y = y
		self.z = z
		self.color = color
	
	def __sub__(self, p):
		return arcPoint(self.x - p.x, self.y - p.y, self.z - p.z, self.color)
	
	def __rsub__(self):
		return arcPoint(-self.x, -self.y, -self.z, self.color)
	
	def __add__(self, p):
		return arcPoint(self.x + p.x, self.y + p.y, self.z + p.z, self.color)
		
	def __str__(self):
		return '<' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + '>'
		
	def vectorProduct(self, p):
		newPoint = arcPoint(self.x, self.y, self.z, self.color)
		
		newPoint.x = self.y*p.z - p.y*self.z
		newPoint.y = self.z*p.x - p.z*self.x
		newPoint.z = self.x*p.y - p.x*self.y
		
		return newPoint

class arcCanvasWindow(QWidget):
	
	def __init__(self, title='New Canvas Window', width=600, height=400, x=100, y=200):
		
		super(arcCanvasWindow, self).__init__()
		
		self.backgroundBrush = Qt.black
		self.points = set([])
		
		self.displayFunct = None
		
		#default
		self.minX = -5
		self.maxX = 5
		
		self.minY = -5
		self.maxY = 5
		
		self.minZ = -5
		self.maxZ = 5
		
		self.projection_mode = 0
		
		self.cameraPosition = arcPoint(0, 0, 1)
		
		self.cameraPointAt = arcPoint(0, 0, 0)
		self.cameraUp = arcPoint(0, 1, 0)
		
		self.calculateCameraBaseVectors()
		
		self.initUI(title, width, height, x, y)
	
	def setWorldSpace(self, minX, maxX, minY, maxY, minZ, maxZ):
		self.minX = minX
		self.maxX = maxX
		
		self.minY = minY
		self.maxY = maxY
		
		self.minZ = minZ
		self.maxZ = maxZ
		
		self.calculateCameraBaseVectors()
	
	def setCameraPosition(self, x, y, z):
		self.cameraPosition = arcPoint(x, y, z)
		self.calculateCameraBaseVectors()
	
	def pointCameraAt(self, x, y, z):
		self.cameraPointAt = arcNormalize(arcPoint(x, y, z))
		self.calculateCameraBaseVectors()
	
	def setCameraUpVector(self, x, y, z):
		self.cameraUp = arcNormalize(arcPoint(x, y, z))
		self.calculateCameraBaseVectors()
	
	def calculateCameraBaseVectors(self):
		self.w = arcNormalize(self.cameraPosition - self.cameraPointAt)
		self.u = arcNormalize(self.cameraUp.vectorProduct(self.w))
		self.v = self.w.vectorProduct(self.u)
		
		tempPoint = arcPoint(self.u.x*self.cameraPosition.x + self.u.y*self.cameraPosition.y + self.u.z*self.cameraPosition.z, 
						self.v.x*self.cameraPosition.x + self.v.y*self.cameraPosition.y + self.v.z*self.cameraPosition.z,
						self.w.x*self.cameraPosition.x + self.w.y*self.cameraPosition.y + self.w.z*self.cameraPosition.z)
		
		self.worldToCameraMatrix = [
									[self.u.x,	self.u.y,	self.u.z,	-tempPoint.x],
									[self.v.x,	self.v.y,	self.v.z,	-tempPoint.y],
									[self.w.x,	self.w.y,	self.w.z,	-tempPoint.z],
									[0,			0,			0,			1]
									]
			
		self.widthRatio = self.width()/(self.maxX-self.minX)
		self.heightRatio = self.height()/(self.maxY-self.minY)
		
		
		
	def initUI(self, title, width, height, x, y):
		self.setWindowTitle(title)
		self.setGeometry(x, y, width, height)
		self.show()
		
		
	def setDisplayFunction(self, displayFunct):
		self.displayFunct = displayFunct
		
	def paintEvent(self, e):
		global points
		qpainter = QPainter()
	
		qpainter.begin(self)
		
		
		#Draw background
		qpainter.setBrush(self.backgroundBrush)
		qpainter.drawRect(QRect(0, 0, self.width(), self.height()))
		
		
		if self.displayFunct is not None:
			self.displayFunct()
		
		for p in points:
			qpainter.setPen(p.color)
			newPoint = arcMultiplyMatrices(self.worldToCameraMatrix, [[p.x], [p.y], [p.z], [1]])
			if self.projection_mode == 0:
				x = int(self.widthRatio*newPoint[0][0] + self.widthRatio*(-self.minX)) 
				y = int(self.heightRatio*newPoint[1][0] + self.heightRatio*(-self.minY))
			else:
				x = 1
				y = 1
			qpainter.drawPoint(x, y)
		
		points = []
		qpainter.end()
	
	def setBackgroundBrush(self, color):
		'''Sets the background color to the specified QBrush
			Keyword arguments:
			    color -- the QBrush or QColor to be used to paint the background
		'''
		self.backgroundBrush = color
	
	def closeEvent(self, *args, **kwargs):
		self.emit(SIGNAL('closing()'))
		
		return QWidget.closeEvent(self, *args, **kwargs)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	image = arcCanvasWindow('arcGL - Adrian Revuelta Cuauhtli')
	
	
	sys.exit(app.exec_())