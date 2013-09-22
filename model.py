from numpy import *

from collada import Collada
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

import render
import physics

class Model(object):
    def __init__(self, filename):
        dae = Collada(filename)
        self.parts = []
        self.triangles = []

        for geometry in dae.scene.objects('geometry'):
            for triset in geometry.primitives():
                if triset.normal_index is not None:
                    mesh = render.Mesh(triset.vertex_index, triset.vertex, triset.texcoord_indexset[0], triset.texcoordset[0], triset.normal_index, triset.normal)
                    effect = triset.material.effect
                    texture = None
                    if len(effect.params) > 0 and mesh.count%3 == 0 and mesh.count > 0:
                        texture = effect.params[0].image.pilimage
                        part = render.ModelPart(mesh, texture)
                        self.parts.append(part)

                        for triangle in triset.vertex_index:
                            tri = physics.Triangle(triset.vertex[triangle])
                            if tri.norm.dot(tri.norm) != 0:
                                self.triangles.append(tri)
    
    def renderables(self):
        for part in self.parts:
            yield part
    
    def collideables(self):
        for tri in self.triangles:
            yield tri
