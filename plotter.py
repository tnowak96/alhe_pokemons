"""
=============================================
Generate polygons to fill under 3D line graph
=============================================

Demonstrate how to create polygons which fill the space under a line
graph. In this example polygons are semi-transparent, creating a sort
of 'jagged stained glass' effect.
"""
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np

matplotlib.use('Qt5Agg')
fig = plt.figure()
ax = fig.gca(projection='3d')


def cc(arg):
    return mcolors.to_rgba(arg, alpha=0.6)
def draw_3D_plot(z_values):

    x_steps, y_steps = z_values.shape[0], z_values.shape[1]
    xs = np.arange(0, x_steps, 1)
    # print(xs)
    # print(type(xs))
    verts = []
    ys = list(range(y_steps))
    # print(type(ys))
    xs = np.insert(xs, 0, xs[0])
    xs = np.append(xs,xs[-1])
    for z in range(z_values.shape[1]):
        zs = z_values[:,z]
        zs = np.insert(zs, 0, 0)
        zs = np.append(zs,0)
        verts.append(list(zip(xs, zs)))

    poly = PolyCollection(verts, facecolors=[cc('r'), cc('g'), cc('b'),
                                             cc('c'), cc('m'), cc('y'), cc('black')])
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=ys, zdir='y')

    ax.set_xlabel('X')
    ax.set_xlim3d(0, x_steps-1)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-1, y_steps)
    ax.set_zlabel('Z')
    ax.set_zlim3d(0, max(z_values.flatten()))

    plt.show()

if __name__ == '__main__':
    if __name__ == '__main__':
        z_values = np.random.rand(100,7)
        draw_3D_plot(z_values)

