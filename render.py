from numpy import *

from collada import Collada
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

def flatten(l):
    return [item for sublist in l for item in sublist]

class Shader(object):
    def __init__(self, filename, enum):
        #self.id = glCreateShader(enum)
        source = open(filename, "r").read()
        strings = [source]
        #count = len(strings)
        #strings = (c_char_p * count)(*strings)
        #c_strings = cast(pointer(strings), POINTER(POINTER(c_char)))
        #glShaderSource(self.id, count, c_strings, None)
        self.shader = shaders.compileShader(strings, enum)
        
        # temp = c_int(0)
        # # retrieve the compile status
        # glGetShaderiv(self.id, GL_COMPILE_STATUS, byref(temp))
 
        # # if compilation failed, print the log
        # if not temp:
        #     # retrieve the log length
        #     glGetShaderiv(self.id, GL_INFO_LOG_LENGTH, byref(temp))
        #     # create a buffer for the log
        #     buffer = create_string_buffer(temp.value)
        #     # retrieve the log text
        #     glGetShaderInfoLog(self.id, temp, None, buffer)
        #     # print the log to the console
        #     print buffer.value

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
    def __init__(self, shader, texture):
        self.shader = shader
        self.texture = texture

class Mesh(object):
    def __init__(self, vert_indices, vertices, norm_indices, normals):
        vert_indices = flatten(vert_indices)
        norm_indices = flatten(norm_indices)        
        
        self.count = len(vert_indices)

        data = zeros((self.count,6), 'f')
        for i in xrange(self.count):
            vertex = vertices[vert_indices[i]]
            normal = normals[norm_indices[i]]
            data[i,:] = concatenate((vertex,normal))
        
        self.vbo = vbo.VBO(data)
    
    def draw(self):
        self.vbo.bind()
        try:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableVertexAttribArray( 0 )
            glEnableVertexAttribArray( 1 )
            glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 8*3, self.vbo )
            glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 8*3, self.vbo+8*3 )
            glDrawArrays(
                GL_TRIANGLES, 0, self.count
            )
        finally:
            self.vbo.unbind()

class ModelPart(object):
    def __init__(self, mesh, im):
        self.mesh = mesh
        # try:
        #     ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
        # except SystemError:
        #     ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
        # self.texID = glGenTextures(1)
        # glBindTexture(GL_TEXTURE_2D, self.texID)
        # glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        # glTexImage2D(
        #     GL_TEXTURE_2D, 0, 3, ix, iy, 0,
        #     GL_RGBA, GL_UNSIGNED_BYTE, image
        # )
    
    def draw(self):
        # glEnable(GL_TEXTURE_2D)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        # glBindTexture(GL_TEXTURE_2D, self.texID)
        self.mesh.draw()

class Model(object):
    def __init__(self, filename):
        dae = Collada(filename)
        self.parts = []
        
        for geometry in dae.scene.objects('geometry'):
            for triset in geometry.primitives():
                if triset.normal_index is not None:
                    mesh = Mesh(triset.vertex_index, triset.vertex, triset.normal_index, triset.normal)
                    effect = triset.material.effect
                    texture = None
                    if len(effect.params) > 0:
                        texture = effect.params[0].image.pilimage
                    part = ModelPart(mesh, texture)
                    self.parts.append(part)
    
    def renderables(self):
        for part in self.parts:
            yield part
