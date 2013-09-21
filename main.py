import math
import numpy
import pygame
from pygame.locals import *

from render import Model, FragmentShader, VertexShader, Program
from transformations import projection_matrix, translation_matrix, rotation_matrix, identity_matrix
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
screen = pygame.display.set_mode((800, 600), HWSURFACE | OPENGL | DOUBLEBUF)

model = Model("models/pyramid.dae")
vert = VertexShader("basic.vert")
frag = FragmentShader("basic.frag")
shader = Program(vert, frag)

vbo = OpenGL.arrays.vbo.VBO(
    numpy.array( [
        [  0, 1, 0 ],
        [ -1,-1, 0 ],
        [  1,-1, 0 ],
        [  2,-1, 0 ],
        [  4,-1, 0 ],
        [  4, 1, 0 ],
        [  2,-1, 0 ],
        [  4, 1, 0 ],
        [  2, 1, 0 ],
    ],'f')
)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
    
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glDisable(GL_DEPTH_TEST)

    shader.use()

    #fov = 90
    #point = [0, 0, 0]
    #normal = [0, 0, 1]
    #perspective_point = [0, 0, -1/math.tan(fov/2)]
    #proj_matrix = projection_matrix(point, normal, perspective=perspective_point)
    #proj_matrix = identity_matrix() #.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    #proj_matrix.astype(numpy.float32)
    #proj_matrix_p = proj_matrix.ctypes.data_as(c_float_p)
    #for i in proj_matrix_p:
        #print(i)
    #proj_loc = glGetUniformLocation(shader.id, "projection_matrix")
    #glUniformMatrix4fv(proj_loc, 1, False, proj_matrix_p)

    #mv_matrix = translation_matrix([0, 0, -5000])
    #mv_matrix *= rotation_matrix(-80, [1, 0, 0])
    #mv_matrix = identity_matrix() #.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    #mv_matrix.astype(numpy.float32)
    #mv_matrix_p = proj_matrix.ctypes.data_as(c_float_p)
    #mv_loc = glGetUniformLocation(shader.id, "modelview_matrix")
    #glUniformMatrix4fv(mv_loc, 1, False, mv_matrix_p)

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #light_pos = numpy.array([0, 1000, 0]).ctypes.data_as(POINTER(c_float))
    #glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    #light_diffuse = numpy.array([1, 1, 1, 1.0]).ctypes.data_as(POINTER(c_float))
    #glMaterialfv(GL_FRONT, GL_DIFFUSE, light_diffuse);



    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65, 800/600, 1, 10000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -100)
    glRotatef(-80, 1, 0, 0)

    for renderable in model.renderables():
        renderable.draw()
    
    pygame.display.flip()
    
    clock.tick(30)
