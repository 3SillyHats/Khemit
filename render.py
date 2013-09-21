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
    def __init__(self, indices, vertices):
        numVerts = len(vertices) / 3
        self.vertices = vbo.VBO(array(vertices, 'f'))
        self.indices = vbo.VBO(array(indices, 'i2'), target=GL_ELEMENT_ARRAY_BUFFER)
        self.count = len(flatten(indices))
    
    def draw(self):
        self.vertices.bind()
        self.indices.bind()
        try:
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointerf( self.vertices )
            glDrawElements(
                GL_TRIANGLES, self.count,
                GL_UNSIGNED_SHORT, self.indices
            )
        finally:
            self.vertices.unbind()
            self.indices.unbind()

class ModelPart(object):
        def __init__(self, mesh):
            self.mesh = mesh

class Model(object):
    def __init__(self, filename):
        dae = Collada(filename)
        self.parts = []
        
        for geometry in dae.geometries:
            triset = geometry.primitives[0]
            mesh = Mesh(triset.vertex_index, triset.vertex)
            part = ModelPart(mesh)
            self.parts.append(part)
    
    def renderables(self):
        for part in self.parts:
            yield part.mesh
