from geometry import Vector2D, Triangle

class UnstructuredMesh(object):
    def __init__(self, nodes=[], elems=[]):
        self.nodes = nodes
        self.elems = elems
        self.triangles = []

        for elem in elems:
            self.triangles.append(Triangle([Vector2D(nodes[elem[0]]),
                                            Vector2D(nodes[elem[1]]),
                                            Vector2D(nodes[elem[2]])]))

    def write_tecplot_file(self, filename):
        with open(filename, 'w') as f:
            f.write('title = "{}"\n'.format(filename))
            f.write('variables = "x", "y"\n')
            f.write(
                'zone t = "mesh" n = {}, e = {}, datapacking = point, zonetype = fetriangle\n'.format(len(self.nodes),
                                                                                                      len(self.elems)))
            for node in self.nodes:
                f.write('{} {}\n'.format(node.x, node.y))

            for elem in self.elems:
                f.write('{} {} {}\n'.format(*(elem + 1)))

if __name__ == '__main__':
    from random import random
    import numpy as np
    from scipy.spatial import Delaunay

    npts = 10000
    nodes = np.array([random() for i in xrange(npts)]).reshape((npts/2, 2))

    elems = Delaunay(nodes).simplices
    nodes = [Vector2D(x, y) for x, y in nodes]

    mesh = UnstructuredMesh(nodes=nodes, elems=elems)
    mesh.write_tecplot_file('test.dat')