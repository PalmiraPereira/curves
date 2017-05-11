from geometry import Vector2D, Triangle


class UnstructuredMesh(object):
    def __init__(self, nodes=[], elems=[]):
        self.nodes = nodes
        self.elems = elems
        self.triangles = []
        self.fields = {}

        for elem in elems:
            self.triangles.append(Triangle([nodes[elem[0]],
                                            nodes[elem[1]],
                                            nodes[elem[2]]]))

    def add_field(self, fieldname):
        self.fields[fieldname] = np.zeros(len(self.elems))

    def write_tecplot_file(self, filename):
        with open(filename, 'w') as f:
            f.write('title = "{}"\n'.format(filename))
            f.write(('variables = "x", "y"' + ', "{}"' * len(self.fields)).format(*self.fields.keys()) + '\n')
            f.write(
                'zone t = "mesh" n = {}, e = {}, datapacking = block, zonetype = fetriangle\n'.format(len(self.nodes),
                                                                                                      len(self.elems)))

            if len(self.fields) == 1:
                f.write('varlocation = ([3]=cellcentered)\n')
            elif len(self.fields) == 2:
                f.write('varlocation = ([3,4]=cellcentered)\n')
            elif len(self.fields) > 2:
                f.write('varlocation = ([3-{}]=cellcentered)\n'.format(len(self.fields)))

            for node in self.nodes:
                f.write('{}\n'.format(node.x))

            for node in self.nodes:
                f.write('{}\n'.format(node.y))

            for field in self.fields.values():
                f.write('\n'.join(map(str, field)))
                f.write('\n')

            for elem in self.elems:
                f.write('{} {} {}\n'.format(*(elem + 1)))

if __name__ == '__main__':
    from random import random
    import numpy as np
    from scipy.spatial import Delaunay

    npts = 100000
    nodes = np.array([random() for i in xrange(npts)]).reshape((npts / 2, 2))

    elems = Delaunay(nodes).simplices
    nodes = [Vector2D(x, y) for x, y in nodes]

    mesh = UnstructuredMesh(nodes=nodes, elems=elems)
    mesh.add_field('alpha')
    mesh.add_field('kappa')

    mat = np.matrix([[0, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [1, 1, 1, 1]])
    rhs = np.matrix([0, 1, 3, 2]).T
    c = np.linalg.solve(mat, rhs).T

    # do some bilinear stuff
    for tri, i in zip(mesh.triangles, xrange(len(mesh.triangles))):
        x = tri.centroid()
        x = np.matrix([x.x*x.y, x.x, x.y, 1.]).T

        mesh.fields['kappa'][i] = (c*x)[0,0]

    mesh.write_tecplot_file('test.dat')