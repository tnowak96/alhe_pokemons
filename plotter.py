from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import math


def cc(arg):
    return mcolors.to_rgba(arg, alpha=0.6)


def draw_3d_plot(z):
    if z.shape[0] > 100_000:
        size_divider = math.ceil(z.shape[0] / 100_000)
        z = z[::size_divider]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x, y = z.shape[0], z.shape[1]
    xs = np.arange(0, x, 1)
    verts = []
    ys = list(range(y))
    xs = np.insert(xs, 0, xs[0])
    xs = np.append(xs,xs[-1])
    for row in range(z.shape[1]):
        zs = z[:, row]
        zs = np.insert(zs, 0, 0)
        zs = np.append(zs,0)
        verts.append(list(zip(xs, zs)))

    poly = PolyCollection(verts, facecolors=[cc('r'), cc('g'), cc('b'),
                                             cc('c'), cc('m'), cc('y'), cc('black')])
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=ys, zdir='y')
    ax.set_xlabel('X')
    ax.set_xlim3d(0, x-1)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-1, y)
    ax.set_zlabel('Z')
    ax.set_zlim3d(0, max(z.flatten()))

    plt.show()


def draw_2d_plot(z):
    if z.shape[0] > 100_000:
        size_divider = math.ceil(z.shape[0] / 100_000)
        z = z[::size_divider]
    z = np.vstack(([0]*7, z, [0]*7))
    plt.subplot(231)
    plt.fill(np.arange(z.shape[0]), z[:,0], 'r')
    plt.title("Pokemon 1")
    plt.subplot(232)
    plt.fill(np.arange(z.shape[0]), z[:,1], 'g')
    plt.title("Pokemon 2")
    plt.subplot(233)
    plt.fill(np.arange(z.shape[0]), z[:,2], 'b')
    plt.title("Pokemon 3")
    plt.subplot(234)
    plt.fill(np.arange(z.shape[0]), z[:,3], 'c')
    plt.title("Pokemon 4")
    plt.subplot(235)
    plt.fill(np.arange(z.shape[0]), z[:,4], 'm')
    plt.title("Pokemon 5")
    plt.subplot(236)
    plt.fill(np.arange(z.shape[0]), z[:,5], 'y')
    plt.title("Pokemon 6")
    plt.show()
    _, ax = plt.subplots()
    ax.fill_betweenx(z[:,6], np.arange(z.shape[0]))
    plt.title("Cost Function")
    plt.show()


if __name__ == '__main__':
    if __name__ == '__main__':
        z_values = np.random.rand(100,7)
        draw_3D_plot(z_values)

