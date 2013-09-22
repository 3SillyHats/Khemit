from numpy import *
from transformations import clip_matrix, translation_matrix, rotation_matrix, identity_matrix

class Camera(object):
	def __init__(self, x_pos=0, y_pos=0, z_pos=0, x_rot=0, y_rot=0, z_rot=0):
		self.setPos(x_pos, y_pos, z_pos)
		self.setRot(x_rot, y_rot, z_rot)

	def setPos(self,x,y,z=0):
		self.pos = array([x,y,z])

	def setRot(self,x,y,z=0):
		y = min(max(y,-math.pi/2),math.pi/2)
		x = x%(2*math.pi)
		self.rot = array([x,y,z])
		self.norm = [math.cos(x), math.sin(x)]

	def move(self,x,y,z=0):
		self.pos += array([x,y,z])

	def rotate(self,x,y,z=0):
		self.setRot(x+self.rot[0], y+self.rot[1], z+self.rot[2])

	def getNorm(self):
		return self.norm

	def getMatrix(self):
		return rotation_matrix(90 + rot[1], [1.0, 0.0, 0.0]).dot(rotation_matrix(-rot[0], [0.0, 0.0, 1.0]).dot(translation_matrix(-pos)))