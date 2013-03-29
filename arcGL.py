#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QWidget, QPainter, QApplication, QColor
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

polygons = []

sideCount = 1
tempPolygon = []

currentColor = QColor(255, 255, 255)

lights = []

ka = kd = ks = 1.0
ksp = 3.0

def arcSetColor(r, g, b):
	global currentColor
	currentColor = QColor(r, g, b)

def arcSetOmniLight(x, y, z):
	global lights
	lights.append(arcPoint(x, y, z))
	
def arcSetDiffuseConstant(k):
	global kd
	kd = k
	
def arcSetAmbientConstant(k):
	global ka
	ka = k

def arcSetSpecularConstant(k):
	global ks
	ks = k

def arcSetSpecularCoefficient(k):
	global ksp
	ksp = k

def arcClearScreen():
	global polygons
	polygons = []
	
def arcSetPoint(p):
	global polygons, tempPolygon, sideCount 
	p.multMatrix(currentMatrix)
	tempPolygon.append(p)
	if len(tempPolygon) == sideCount:
		polygons.append(tempPolygon)
		tempPolygon = []		
		

def arcBeginPolygon(sides = 3):
	global sideCount
	sideCount = sides
	
def arcEndPolygon():
	global sideCount
	sideCount = 1

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

def arcRotateX(angle, vector=None):
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
	if vector is None:
		currentMatrix = arcMultiplyMatrices(currentMatrix, rotationX)
	else:
		if vector.__class__.__name__ == 'arcPoint':
			vector.multMatrix(rotationX)
		else:
			return arcMultiplyMatrices(rotationX, vector)

def arcRotateY(angle, vector=None):
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
	
	if vector is None:
		currentMatrix = arcMultiplyMatrices(currentMatrix, rotationY)
	else:
		if vector.__class__.__name__ == 'arcPoint':
			vector.multMatrix(rotationY)
		else:
			return arcMultiplyMatrices(rotationY, vector)
	
def arcRotateZ(angle, vector=None):
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
	
	if vector is None:
		currentMatrix = arcMultiplyMatrices(currentMatrix, rotationZ)
	else:
		if vector.__class__.__name__ == 'arcPoint':
			vector.multMatrix(rotationZ)
		else:
			return arcMultiplyMatrices(rotationZ, vector)

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
	global currentColor
	def __init__(self, x, y=0, z=0, color=None):
		if x.__class__.__name__ == 'arcPoint':
			self.x = x.x
			self.y = x.y
			self.z = x.z
			self.color = QColor(x.color.red(), x.color.green(), x.color.blue())
		else:
			self.x = x
			self.y = y
			self.z = z
			if color:
				self.color = QColor(color.red(), color.green(), color.blue())
			else:
				self.color = QColor(currentColor.red(), currentColor.green(), currentColor.blue())
	
	def __sub__(self, p):
		return arcPoint(self.x - p.x, self.y - p.y, self.z - p.z, QColor(self.color.red(), self.color.green(), self.color.blue()))
	
	def __add__(self, p):
		return arcPoint(self.x + p.x, self.y + p.y, self.z + p.z, QColor(self.color.red(), self.color.green(), self.color.blue()))
	
	def __eq__(self, p):
		return self.x == p.x and self.y == p.y and self.z == p.z
	
	def __ne__(self, p):
		return not self.__eq__(p)
	
	def __str__(self):
		return '<' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + '>'
		
	def __repr__(self):
		return '<' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + '>'
	
	def __mul__(self, k):
		return arcPoint(self.x*k, self.y*k, self.z*k, QColor(self.color.red(), self.color.green(), self.color.blue()))
	
	def __rmul__(self, k):
		return arcPoint(self.x*k, self.y*k, self.z*k, QColor(self.color.red(), self.color.green(), self.color.blue()))
		
	
	def dotProduct(self, p):
		return p.x*self.x + p.y*self.y + p.z*self.z
	
	def vectorProduct(self, p):
		newPoint = arcPoint(self.x, self.y, self.z)
		
		newPoint.x = self.y*p.z - p.y*self.z
		if newPoint.x == -0.0:
			newPoint.x = 0.0
		newPoint.y = self.z*p.x - p.z*self.x
		if newPoint.y == -0.0:
			newPoint.y = 0.0
		newPoint.z = self.x*p.y - p.x*self.y
		if newPoint.z == -0.0:
			newPoint.z = 0.0
		
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
		return self
	
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
	
	def initUI(self, title, width, height, x, y):
		self.setWindowTitle(title)
		self.setGeometry(x, y, width, height)
		self.show()
	
	def setWorldSpace(self, minX, maxX, minY, maxY, minZ, maxZ):
		self.minX = minX
		self.maxX = maxX
		
		self.minY = minY
		self.maxY = maxY
		
		self.minZ = minZ
		self.maxZ = maxZ
		
		self.calculateCameraBaseVectors()
	
	def setCameraPosition(self, x, y=None, z=None):
		if x.__class__.__name__ == 'arcPoint':
			self.cameraPosition = x
		else:
			self.cameraPosition = arcPoint(x, y, z)
		self.calculateCameraBaseVectors()
	
	def pointCameraAt(self, x, y, z):
		self.cameraPointAt = arcPoint(x, y, z).normalize()
		self.calculateCameraBaseVectors()
	
	def setCameraUpVector(self, x, y, z):
		self.cameraUp = arcPoint(x, y, z).normalize()
		self.calculateCameraBaseVectors()
	
	def setProjectionMode(self, projectionMode):
		self.projection_mode = projectionMode
		if projectionMode == arcPROJECTION_MODES.ORTOGONAL:
			self.projectionMatrix = [
										[1, 0, 0, 0],
										[0, 1, 0, 0],
										[0, 0, 1, 0],
										[0, 0, 0, 1],
									]
		else:
			raise NotImplementedError('Not yet implemented')
			self.projectionMatrix = [
										[1, 0, 0, 0],
										[0, 1, 0, 0],
										[0, 0, 1, 0],
										[0, 0, 0, 1],
									]
	
	def calculateCameraBaseVectors(self):
		self.w = (self.cameraPosition - self.cameraPointAt).normalize()
		self.u = self.cameraUp.vectorProduct(self.w).normalize()
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
			
		self.widthRatio = 1.0*(self.width()-1)/(self.maxX-self.minX)
		self.heightRatio = 1.0*(self.height()-1)/(self.maxY-self.minY)
		
		
	def setDisplayFunction(self, displayFunct):
		self.displayFunct = displayFunct
		
	def paintEvent(self, e):
		global polygons, currentMatrix, lights, ka, kd, ks, ksp
		qpainter = QPainter()
	
		qpainter.begin(self)
		
		z_buffer = {}
		
		#Draw background
		qpainter.setBrush(self.backgroundBrush)
		qpainter.drawRect(QRect(0, 0, self.width(), self.height()))
		
		
		if self.displayFunct is not None:
			self.displayFunct(self)
		
		polyIndex = 1
		
		for poly in polygons:
			
			points = {}
			lastPoint = None
			
			normal = self.cameraPosition.getNormal()
			
			if len(poly) > 2:
				v1 = poly[1] - poly[0]
				v2 = poly[2] - poly[0]
				normal = v1.vectorProduct(v2).normalize()
				
				otherNormal = v1.vectorProduct(v2).normalize()
				otherNormal.multMatrix(self.worldToCameraMatrix)
				
				p0temp = arcPoint(poly[0].x, poly[0].y, poly[0].z)
				p1temp = arcPoint(poly[1].x, poly[1].y, poly[1].z)
				p2temp = arcPoint(poly[2].x, poly[2].y, poly[2].z)
				
				p0temp.multMatrix(self.worldToCameraMatrix)
				p1temp.multMatrix(self.worldToCameraMatrix)
				p2temp.multMatrix(self.worldToCameraMatrix)
				
				v1temp = p1temp - p0temp
				v2temp = p2temp - p0temp
				
				
				transformedNormal = v1temp.vectorProduct(v2temp).normalize()
				
				if transformedNormal.z < 0:
					continue
				
				
				poly.append(arcPoint(poly[0]))
				
				
			firstPointAdded = False
			
			for p in poly:
				
				I = 1.0
				if len(lights) > 0:
					I = 0.0
					for l in lights:
						lv = l - p
						spec = self.cameraPosition.getNormal().dotProduct(l.getNormal())**ksp
						#ln = l.getNormal()
						#h = 2*normal.dotProduct(ln)*normal - ln
						#spec = self.cameraPosition.getNormal().dotProduct(h)**ksp
						I += (ka + kd*normal.dotProduct(lv.getNormal()) + ks*spec)/3
					I = I/len(lights)
				
				if I <= 0:
					p.color.setRed(0)
					p.color.setGreen(0)
					p.color.setBlue(0)
				else:
					r = p.color.red()*I
					g = p.color.green()*I
					b = p.color.blue()*I
					
					p.color.setRed(r)
					p.color.setGreen(g)
					p.color.setBlue(b)
				
				p.multMatrix(self.worldToCameraMatrix)
				p.multMatrix(self.projectionMatrix)
				
				p.x = int(round(self.widthRatio*p.x + self.widthRatio*(-self.minX)))
				p.y = int(round(self.height() - 1 - (self.heightRatio*p.y + self.heightRatio*(-self.minY))))
				
				if lastPoint is not None and p.y != lastPoint.y:
					mx = p.x - lastPoint.x
					my = p.y - lastPoint.y
					mz = p.z - lastPoint.z
					mRed = p.color.red() - lastPoint.color.red()
					mGreen = p.color.green() - lastPoint.color.green()
					mBlue = p.color.blue() - lastPoint.color.blue()
					s = max(abs(mx), abs(my))
					if s == 0:
						continue
					dx = 1.0*mx/s
					dy = 1.0*my/s
					dz = 1.0*mz/s
					
					dRed = 1.0*mRed/s
					dGreen = 1.0*mGreen/s
					dBlue = 1.0*mBlue/s
					
					for i in range(1, s):
						x = int(lastPoint.x + dx*i)
						y = int(lastPoint.y + dy*i)
						z = lastPoint.z + dz*i
						
						r = lastPoint.color.red() + dRed*i
						g = lastPoint.color.green() + dGreen*i
						b = lastPoint.color.blue() + dBlue*i
						if y in points:
							points[y].append(arcPoint(x, y, z, QColor(r, g, b)))
						else:
							points[y] = [arcPoint(x, y, z, QColor(r, g, b))]
				lastPoint = p
				
				if p == poly[0] and firstPointAdded:
					continue
				firstPointAdded = True
				if p.y in points:
					points[p.y].append(p)
				else:
					points[p.y] = [p]
			
			for y in points.keys():
				p1 = points[y][0]
				if len(points[y]) == 1:
					qpainter.setPen(p1.color)
					if y in z_buffer:
						if p1.x in z_buffer[y]:
							if p1.z > z_buffer[y][p1.x]:
								qpainter.drawPoint(p1.x, y)
								z_buffer[y][p1.x] = p1.z
						else:
							qpainter.drawPoint(p1.x, y)
							z_buffer[y][p1.x] = p1.z
					else:
						z_buffer[y] = {p1.x: p1.z}
						qpainter.drawPoint(p1.x, y)
					continue
				for index in range(1, len(points[y])):
					p1 = points[y][index-1]
					p2 = points[y][index]
					mx = p2.x - p1.x
					mz = p2.z - p1.z
					mRed = p2.color.red() - p1.color.red()
					mGreen = p2.color.green() - p1.color.green()
					mBlue = p2.color.blue() - p1.color.blue()
					s = abs(mx)
					if s == 0:
						continue
					dx = 1.0*mx/s
					dz = 1.0*mz/s
					dRed = 1.0*mRed/s
					dGreen = 1.0*mGreen/s
					dBlue = 1.0*mBlue/s
					if y not in z_buffer:
						z_buffer[y] = {}
					for i in range(0, s+1):
						x = int(p1.x + dx*i)
						z = p1.z + dz*i
						
						r = p1.color.red() + dRed*i
						g = p1.color.green() + dGreen*i
						b = p1.color.blue() + dBlue*i
						qpainter.setPen(QColor(r, g, b))
						if x in z_buffer[y]:
							if z > z_buffer[y][x]:
								qpainter.drawPoint(x, y)
								z_buffer[y][x] = z
						else:
							z_buffer[y][x] = z
							qpainter.drawPoint(x, y)
			polyIndex += 1
		arcClearScreen()
		
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