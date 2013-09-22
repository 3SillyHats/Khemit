from numpy import *

from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

def flatten(l):
    return [item for sublist in l for item in sublist]

class Shader(object):
    def __init__(self, filename, enum):
        source = open(filename, "r").read()
        strings = [source]
        self.shader = shaders.compileShader(strings, enum)

class VertexShader(Shader):
    def __init__(self, filename):
        super(VertexShader, self).__init__(filename, GL_VERTEX_SHADER)

class FragmentShader(Shader):
    def __init__(self, filename):
        super(FragmentShader, self).__init__(filename, GL_FRAGMENT_SHADER)

class Program(object):
    def __init__(self, vertex_shader, fragment_shader):
        self.program = shaders.compileProgram(vertex_shader.shader, fragment_shader.shader)
    
    def use(self):
        shaders.glUseProgram(self.program)

class Material(object):
    def __init__(self, im):
        try:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
        self.texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )
    
    def bind(self, shader):
        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glActiveTexture( GL_TEXTURE0 + 1 )
        glBindTexture(GL_TEXTURE_2D, self.texID)
        tex_loc = glGetUniformLocation(shader.program, "tex")
        glUniform1i(tex_loc, 1)


class Mesh(object):
    def __init__(self, vert_indices, vertices, texture_indices, texture_coordinates, norm_indices, normals):
        vert_indices = flatten(vert_indices)
        norm_indices = flatten(norm_indices)  
        texture_indices = flatten(texture_indices)        
        
        self.count = len(vert_indices)

        data = zeros((self.count,8), 'f')
        for i in xrange(self.count):
            vertex = vertices[vert_indices[i]]
            normal = normals[norm_indices[i]]
            tex_coord = texture_coordinates[texture_indices[i]]
            data[i,:] = concatenate((vertex,normal,array(tex_coord, 'f')))
        
        self.vbo = vbo.VBO(data)
    
    def draw(self):
        self.vbo.bind()
        try:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableVertexAttribArray( 0 )
            glEnableVertexAttribArray( 1 )
            glEnableVertexAttribArray( 2 )
            glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 4*3*2+4*2, self.vbo )
            glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 4*3*2+4*2, self.vbo+4*3 )
            glVertexAttribPointer( 2, 2, GL_FLOAT, GL_FALSE, 4*3*2+4*2, self.vbo+4*3*2 )
            glDrawArrays(
                GL_TRIANGLES, 0, self.count
            )
        finally:
            self.vbo.unbind()

class ModelPart(object):
    def __init__(self, mesh, im):
        self.mesh = mesh
        self.material = Material(im)
            
    def draw(self, shader):
        self.material.bind(shader)
        self.mesh.draw()

