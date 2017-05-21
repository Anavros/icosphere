
from vispy import gloo, io
import rocket
import rocket.aux as aux
from . import icotree



def main():
    global planet, camera, program
    planet = aux.Mover()
    camera = aux.View(fov=45)
    program = aux.load_shaders('shaders/vertex.glsl', 'shaders/fragment.glsl')

    rocket.prep(size=(512, 512))
    camera.move(z=(-6))
    planet.vel = aux.Velocity()
    planet.verts, planet.color, planet.index, planet.lines, planet.sides = buffers()
    planet.sides = aux.buffer(planet.sides)
    planet.index = aux.buffer(planet.index)
    planet.lines = aux.buffer(planet.lines)
    rocket.launch()


def buffers(planet):
    count = 1
    verts = np.zeros(shape=(len(self.faces)*3+1, 3), dtype=np.float32)
    color = np.zeros(shape=(len(self.faces)*3+1, 3), dtype=np.float32)
    index = np.zeros(shape=(len(self.faces)*3+1),    dtype=np.uint32)
    lines = np.zeros(shape=(len(self.faces)*3+1, 2), dtype=np.uint32)
    sides = np.zeros(shape=(len(self.faces)*3+1),    dtype=np.uint32)
    verts[0, :] = [0, 0, 0]  # origin point
    color[0, :] = [0, 0, 0]
    for face in self.faces:
        for i, node in enumerate(face):
            verts[count+i, :] = tuple(node)
            index[count+i-1] = count+i
        sides[count-1:count-1+3] = [0, count+1, count+2]
        try:
            face_color = self.colors[face.group]
        except KeyError:
            face_color = np.random.random(3)
        color[count:count+3] = face_color  # set all three nodes to same color
        count += 3
    return verts, color, index, lines, sides


@rocket.attach
def update():
    """Update the game. Called for every frame, usually sixty per second."""
    planet.rotate(*tuple(planet.vel))
    planet.vel.damp()


@rocket.attach
def draw():
    program['a_position'] = planet.verts
    program['a_coloring'] = planet.color

    program['m_model'] = planet.transform
    program['m_view'] = camera.transform
    program['m_proj'] = camera.proj

    program['u_color'] = (0.5, 0.6, 0.7); program.draw('triangles', planet.index)
    program['u_color'] = (0.4, 0.5, 0.6); program.draw('triangles', planet.sides)
    #program['u_color'] = (0.2, 0.3, 0.4); program.draw('lines', planet.lines)
    #program['u_color'] = (0.0, 0.0, 0.1); program.draw('points')


@rocket.attach
def key_press(key):
    if key == 'R':
        pass


@rocket.attach
def left_drag(start, end, delta):
    planet.vel.accel(x=delta[0]/5, y=delta[1]/5)


@rocket.attach
def right_drag(start, end, delta):
    planet.rotate(z=(0-delta[1])/2)


@rocket.attach
def middle_drag(start, end, delta):
    planet.rotate(x=delta[0], y=delta[1])
    planet.vel.decel(100, 100, 100)


@rocket.attach
def scroll(point, direction):
    camera.move(0, 0, direction/10)


if __name__ == '__main__':
    main()
