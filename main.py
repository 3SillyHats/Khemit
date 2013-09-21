import math
import numpy
import pygame
from pygame.locals import *

from render import Model, FragmentShader, VertexShader, Program
from transformations import clip_matrix, translation_matrix, rotation_matrix, identity_matrix
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
screen = pygame.display.set_mode((800, 600), HWSURFACE | OPENGL | DOUBLEBUF)
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

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

TURN_SPEED = 1.5
MOVE_SPEED = 0.1
x_facing = 0.
y_facing = 0.
x_norm = 1.
y_norm = 0.

x_pos = 50.
y_pos = 0.
z_pos = 2.

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()

    delta_x, delta_y = pygame.mouse.get_rel()

    if(delta_y != 0):
        y_facing = min(max(y_facing + TURN_SPEED*delta_y,-math.pi/2),math.pi/2)
    if(delta_x != 0):
        x_facing = (x_facing + TURN_SPEED*delta_x)%(2*math.pi)
        facing_norm[0], facing_norm[1] = math.cos(x_facing), math.sin(x_facing)
    
    keyDown = pygame.key.get_pressed()

    if keyDown[pygame.K_w]:
        x_pos += MOVE_SPEED * x_norm;
        y_pos += MOVE_SPEED * y_norm;
    if keyDown[pygame.K_s]:
        x_pos -= MOVE_SPEED * x_norm;
        y_pos -= MOVE_SPEED * y_norm;
    if keyDown[pygame.K_a]:
        x_pos += MOVE_SPEED * y_norm;
        y_pos -= MOVE_SPEED * x_norm;
    if keyDown[pygame.K_d]:
        x_pos -= MOVE_SPEED * y_norm;
        y_pos += MOVE_SPEED * x_norm;

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT) #?!
    glEnable(GL_DEPTH_TEST)

    shader.use()

    fov = 65.0
    aspect = 800.0/600.0
    near = 1.0
    far = 10000.0
    right = near * math.tan(fov*math.pi/360.0)
    left = -right
    top = right / aspect
    bottom = -top
    proj_matrix = clip_matrix(left, right, bottom, top, near, far, perspective=True)
    proj_loc = glGetUniformLocation(shader.program, "projection_matrix")
    glUniformMatrix4fv(proj_loc, 1, False, numpy.array(proj_matrix, 'f'))

    mv_matrix = rotation_matrix(90 + y_facing, [1.0, 0.0, 0.0]).dot(rotation_matrix(-x_facing, [0.0, 0.0, 1.0]).dot(translation_matrix([-x_pos, -y_pos, -z_pos])))
    mv_loc = glGetUniformLocation(shader.program, "modelview_matrix")
    glUniformMatrix4fv(mv_loc, 1, True, numpy.array(mv_matrix, 'f'))

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #glLightfv(GL_LIGHT0, GL_POSITION, [0,100, 100])
    #glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0, 1, 1.0]);

    for renderable in model.renderables():
        renderable.draw()
    
    pygame.display.flip()
    
    clock.tick(30)
