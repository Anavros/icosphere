
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
    return np.dot(matrix, transforms.translate((x, y, z)))


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
    def __init__(self, proj='perspective', fov=45.0, aspect=1.0, near=1.0, far=20.0):
        Mover.__init__(self)
        if proj == 'orthographic':
            self.proj = transforms.ortho(0, 1, 0, 1, 0, 1)
        elif proj == 'perspective':
            self.proj = transforms.perspective(fov, aspect, near, far)


class Storage:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v


class Atlas:
    def __init__(self, width, height, cols, rows):
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.tex = np.zeros((cols*width, rows*height, 4), dtype=np.uint8)

    def insert(self, image, col, row):
        x_off = col*self.width
        y_off = row*self.height
        self.tex[y_off:y_off+self.height, x_off:x_off+self.width, :] = image

    def coords(self, col, row):
        tex_w = 1/self.cols
        tex_h = 1/self.rows
        return np.array([
            (tex_w*col, tex_h*row), (tex_w*col+tex_w, tex_h*row),
            (tex_w*col, tex_h*row+tex_h), (tex_w*col+tex_w, tex_h*row+tex_h),
        ], dtype=np.float32)

    def get_full_texture(self):
        return None

    def get(self, col, row):
        x_off = col*self.width
        y_off = row*self.height
        return self.tex[y_off:y_off+self.height, x_off:x_off+self.width, :]


class LookupAtlas:
    def __init__(self, size, rows):
        if size*rows not in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
            raise Warning("Atlas size is not a power of two!")
        self.size = size
        self.rows = rows
        self.texture = np.zeros((size*rows, size*rows, 4), dtype=np.uint8)
        self._x = 0
        self._y = 0
        self.lookup = {}

    def insert(self, image, tag):
        x = self.size * self._x
        y = self.size * self._y
        if image.shape[0] != self.size or image.shape[1] != self.size:
            raise ValueError("Can not insert wrongly sized image!")

        print(x, y)
        print(self.size)
        self.texture[y:y+self.size, x:x+self.size, :] = image
        # record location for lookup
        if tag not in self.lookup.keys():
            self.lookup[tag] = [(x, y)]
        else:
            self.lookup[tag].append((x, y))
        # move pointer
        if self._x+1 < self.rows:
            self._x += 1
        else:
            if self._y+1 < self.rows:
                self._x = 0
                self._y += 1
            else:
                raise ValueError("Texture atlas is full! Can not insert new image.")

    def locate(self, tag, n):
        return self.lookup[tag][n]


class Cycler:
    def __init__(self, items=None):
        self.items = {}
        if items is not None:
            for key, value_list in items.items():
                self.add(key, value_list)

    def add(self, key, items):
        self.items[key] = {'n': 0, 'count': len(items), 'items': items}

    def get(self, key):
        n = self.items[key]['n']
        return self.items[key]['items'][n]

    def count(self, key):
        return self.items[key]['count']

    def cycle(self, key):
        n = self.items[key]['n']
        c = self.items[key]['count']
        self.items[key]['n'] = (n+1) % c


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
