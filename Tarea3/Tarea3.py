#!/usr/bin/python
# -*- coding: utf-8 -*-

from arcGL import *
from threading import Timer
from PyQt4 import QtCore


currentAngle = 0
deltaTime = 0.1
angleTimer = None

def displayFunct(canvas):
	
	arcPushMatrix()
	
	arcRotateY(currentAngle)
	
	arcSetPoint(arcPoint(-2, -2, 2))
	arcSetPoint(arcPoint(-2, -2, -2))
	arcSetPoint(arcPoint(2, -2, -2))
	arcSetPoint(arcPoint(2, -2, 2))
	
	arcSetPoint(arcPoint(-2, 2, 2))
	arcSetPoint(arcPoint(-2, 2, -2))
	arcSetPoint(arcPoint(2, 2, -2))
	arcSetPoint(arcPoint(2, 2, 2))
	
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
	canvas = arcCanvasWindow('Tarea 3 - Adrian Revuelta Cuauhtli', width=600, height=600)
	
	canvas.setWorldSpace(-5, 5, -5, 5, -5, 5)
	canvas.setCameraPosition(4, 3, 3)
	canvas.pointCameraAt(0, 0, 0)
	canvas.setCameraUpVector(0, 1, 0)
	
	canvas.setDisplayFunction(displayFunct)
	
	angleTimer = Timer(deltaTime, increaseAngle, args=[canvas])
	angleTimer.start()
	canvas.connect(canvas, QtCore.SIGNAL('closing()'), stopTimerSlot)
	
	sys.exit(app.exec_())
