#!/usr/bin/python
# -*- coding: utf-8 -*-

from arcGL import *
from threading import Timer
from PyQt4 import QtCore


currentAngle = 0
deltaTime = 0.1
angleTimer = None

cameraPos = arcPoint(4, 3, 3)

def displayFunct(canvas):
	global cameraPos, currentAngle
	
	arcPushMatrix()
	
	arcRotateY(currentAngle/2)
	
	#arcRotateY(currentAngle, cameraPos)
	
	#canvas.setCameraPosition(cameraPos)
	
	arcBeginPolygon(4)
	
	arcSetColor(0, 255, 0)
	
	arcSetPoint(arcPoint(2, 2, 2))
	arcSetPoint(arcPoint(-2, 2, 2))
	arcSetPoint(arcPoint(-2, -2, 2))
	arcSetPoint(arcPoint(2, -2, 2))
	
	arcSetPoint(arcPoint(2, 2, -2))
	arcSetPoint(arcPoint(2, 2, 2))
	arcSetPoint(arcPoint(2, -2, 2))
	arcSetPoint(arcPoint(2, -2, -2))
	
	arcSetPoint(arcPoint(-2, 2, 2))
	arcSetPoint(arcPoint(-2, 2, -2))
	arcSetPoint(arcPoint(-2, -2, -2))
	arcSetPoint(arcPoint(-2, -2, 2))
	
	arcSetPoint(arcPoint(-2, 2, -2))
	arcSetPoint(arcPoint(2, 2, -2))
	arcSetPoint(arcPoint(2, -2, -2))
	arcSetPoint(arcPoint(-2, -2, -2))
	
	arcSetPoint(arcPoint(2, 2, -2))
	arcSetPoint(arcPoint(-2, 2, -2))
	arcSetPoint(arcPoint(-2, 2, 2))
	arcSetPoint(arcPoint(2, 2, 2))
	
	arcSetPoint(arcPoint(2, -2, 2))
	arcSetPoint(arcPoint(-2, -2, 2))
	arcSetPoint(arcPoint(-2, -2, -2))
	arcSetPoint(arcPoint(2, -2, -2))
	
	arcEndPolygon()
	
	
	arcPopMatrix()

def increaseAngle(canvas):
	global currentAngle, angleTimer
	
	deltaAngle =  5
	
	if currentAngle >= 360:
		currentAngle = 0
	currentAngle += deltaAngle
	canvas.update()
	angleTimer = Timer(deltaTime, increaseAngle, args=[canvas])
	angleTimer.start()

def stopTimerSlot():
	global angleTimer
	
	angleTimer.cancel()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	canvas = arcCanvasWindow('Tarea 4 - Adrian Revuelta Cuauhtli', width=600, height=600)
	
	canvas.setWorldSpace(-5, 5, -5, 5, -5, 5)
	canvas.setCameraUpVector(0, 1, 0)
	canvas.pointCameraAt(0, 0, 0)
	canvas.setCameraPosition(cameraPos)
	
	arcSetOmniLight(5, 4, 4)
	
	canvas.setDisplayFunction(displayFunct)
	
	angleTimer = Timer(deltaTime, increaseAngle, args=[canvas])
	angleTimer.start()
	canvas.connect(canvas, QtCore.SIGNAL('closing()'), stopTimerSlot)
	
	sys.exit(app.exec_())