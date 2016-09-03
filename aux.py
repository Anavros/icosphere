
import numpy as np
from vispy import gloo
from vispy.util import transforms


def buffer(array, method='index'):
    return gloo.IndexBuffer(array)


def load_shaders(v_path, f_path):
    """Load shaders from the disk and return them as a gloo program."""
    with open(v_path, 'r') as v_file:
        v_string = v_file.read()
    with open(f_path, 'r') as f_file:
        f_string = f_file.read()
    return gloo.Program(v_string, f_string)


def delta(v1, v2):
    return abs(v1[0] - v2[0]), abs(v1[1] - v2[1])

def move(matrix, x=0, y=0, z=0):
    return np.dot(matrix, transforms.translate((y, x, z)))

def rotate(matrix, x=0, y=0, z=0):
    matrix = np.dot(matrix, transforms.rotate(x, (0, 1, 0)))
    matrix = np.dot(matrix, transforms.rotate(y, (1, 0, 0)))
    matrix = np.dot(matrix, transforms.rotate(z, (0, 0, 1)))
    return matrix

def scale(matrix, x=0, y=0, z=0):
    return np.dot(matrix, transforms.scale((x, y, z)))

class Mover:
    def __init__(self):
        self.transform = np.eye(4)

    def move(self, x=0, y=0, z=0):
        self.transform = move(self.transform, x, y, z)

    def rotate(self, x=0, y=0, z=0):
        self.transform = rotate(self.transform, x, y, z)

    def scale(self, x=0, y=0, z=0):
        self.transform = scale(self.transform, x, y, z)

class View(Mover):
    def __init__(self, fov=45.0, aspect_ratio=1.0, near=1.0, far=20.0):
        Mover.__init__(self)
        self.proj = transforms.perspective(fov, aspect_ratio, near, far)

class Storage:
    pass

class Vector:
    pass

class Payload:
    """
    Container for in-world object data.

    Includes functions for various two- and three-dimensional transformations.
    """


class Velocity:
    """
    Small container for object velocity data.

    Contains functions for acceleration and damping.
    """
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        for a in [self.x, self.y, self.z]:
            yield a

    def damp(self, n=0.95):
        self.x *= n if abs(self.x) > 0.1 else 0
        self.y *= n if abs(self.y) > 0.1 else 0
        self.z *= n if abs(self.z) > 0.1 else 0

    def accel(self, x=0, y=0, z=0):
        self.x += x
        self.y += y
        self.z += z

    def decel(self, x=0, y=0, z=0):
        self.x = max(self.x-x, 0)
        self.y = max(self.y-y, 0)
        self.z = max(self.z-z, 0)
