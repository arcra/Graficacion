#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QWidget, QPainter, QApplication
from PyQt4.QtCore import Qt, QRect, SIGNAL
from math import sin, cos, pi, sqrt

def enum(**enums):
	return type('Enum', (), enums)

arcPROJECTION_MODES = enum(ORTOGONAL=0, PERSPECTIVE=1)

matrixStack = []
currentMatrix = [	[1, 0, 0, 0],
					[0, 1, 0, 0],
					[0, 0, 1, 0],
					[0, 0, 0, 1]
				]

points = []

def arcSetPoint(p):
	global points
	p.multMatrix(currentMatrix)
	points.append(p)

def arcPushMatrix():
	global matrixStack, currentMatrix
	matrixStack.append(currentMatrix)

def arcPopMatrix():
	global matrixStack, currentMatrix
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
	for index in range(1, len(matrices)):
		tempM = []
		for row in range(len(M)):
			tempM.append([])
			for column in range(len(matrices[index][0])):
				value = 0
				for m in range(len(M[0])):
					value += M[row][m]*matrices[index][m][column]
				tempM[row].append(value)
		M = tempM
	return M

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
		
	
	def dotProduct(self, p):
		return p.x*self.x + p.y*self.y + p.z*self.z
	
	def vectorProduct(self, p):
		newPoint = arcPoint(self.x, self.y, self.z, self.color)
		
		newPoint.x = self.y*p.z - p.y*self.z
		newPoint.y = self.z*p.x - p.z*self.x
		newPoint.z = self.x*p.y - p.x*self.y
		
		return newPoint
	
	def multMatrix(self, matrix):
		newPoint = arcMultiplyMatrices(matrix, [[self.x], [self.y], [self.z], [1]])
		self.x = newPoint[0][0]
		self.y = newPoint[1][0]
		self.z = newPoint[2][0]
	
	def normalize(self):
		norm = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
		if norm > 0:
			self.x = self.x/norm
			self.y = self.y/norm
			self.z = self.z/norm
	
	def getNormal(self):
		norm = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
		p = arcPoint(self.x, self.y, self.z, self.color)
		if norm > 0:
			p.x = p.x/norm
			p.y = p.y/norm
			p.z = p.z/norm
		
		return p

class arcCanvasWindow(QWidget):
	
	def __init__(self, title='New Canvas Window', width=600, height=400, x=100, y=200):
		global arcPROJECTION_MODES
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
		
		self.setProjectionMode(arcPROJECTION_MODES.ORTOGONAL)
		
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
		self.cameraPointAt = arcPoint(x, y, z).getNormal()
		self.calculateCameraBaseVectors()
	
	def setCameraUpVector(self, x, y, z):
		self.cameraUp = arcPoint(x, y, z).getNormal()
		self.calculateCameraBaseVectors()
	
	def setProjectionMode(self, projectionMode):
		self.projection_mode = projectionMode
		if projectionMode == arcPROJECTION_MODES.ORTOGONAL:
			self.projectionMatrix = [
										[1, 0, 0, 0],
										[0, 1, 0, 0],
										[0, 0, 0, 0],
										[0, 0, 0, 1],
									]
		else:
			raise NotImplementedError('Not yet implemented')
			self.projectionMatrix = [
										[1, 0, 0, 0],
										[0, 1, 0, 0],
										[0, 0, 0, 0],
										[0, 0, 0, 1],
									]
	
	def calculateCameraBaseVectors(self):
		self.w = (self.cameraPosition - self.cameraPointAt).getNormal()
		self.u = self.cameraUp.vectorProduct(self.w).getNormal()
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
			p.multMatrix(self.worldToCameraMatrix)
			p.multMatrix(self.projectionMatrix)
			x = int(self.widthRatio*p.x + self.widthRatio*(-self.minX)) 
			y = int(self.heightRatio*p.y + self.heightRatio*(-self.minY))
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