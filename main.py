import math
import numpy
import pygame
import camera
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

TURN_SPEED = 0.1
MOVE_SPEED = 0.1
camera = camera.Camera(50,0,2, 0,0,0)

shader.use()
li_loc = glGetUniformLocation(shader.program, "light_intensity")
glUniform4f(li_loc, 1.0, 1.0, 1.0, 1.0)

light_direction = numpy.array([1, 0, 0, 0], 'f')

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()

    delta_x, delta_y = pygame.mouse.get_rel()

    camera.rotate(delta_x*TURN_SPEED, delta_y*TURN_SPEED)

    keyDown = pygame.key.get_pressed()
    norm = camera.getNorm()

    dx, dy = 0,0

    if keyDown[pygame.K_w]:
        dx += MOVE_SPEED * norm[0];
        dy += MOVE_SPEED * norm[1];
    if keyDown[pygame.K_s]:
        dx -= MOVE_SPEED * norm[0];
        dy -= MOVE_SPEED * norm[1];
    if keyDown[pygame.K_a]:
        dx += MOVE_SPEED * norm[1];
        dy -= MOVE_SPEED * norm[0];
    if keyDown[pygame.K_d]:
        dx -= MOVE_SPEED * norm[1];
        dy += MOVE_SPEED * norm[0];

    camera.move(dx,dy)

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

    mv_matrix = camera.getMatrix()
    mv_loc = glGetUniformLocation(shader.program, "modelview_matrix")
    glUniformMatrix4fv(mv_loc, 1, True, numpy.array(mv_matrix, 'f'))

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #glLightfv(GL_LIGHT0, GL_POSITION, [0,100, 100])
    #glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0, 1, 1.0]);

    light_dir_camera_space = mv_matrix.dot(light_direction)
    ld_loc = glGetUniformLocation(shader.program, "dir_to_light")
    glUniform3fv(ld_loc, 1, numpy.array(light_dir_camera_space[:3]))

    for renderable in model.renderables():
        renderable.draw()
    
    pygame.display.flip()
    
    clock.tick(30)
