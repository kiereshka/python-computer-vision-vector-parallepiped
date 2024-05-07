import numpy as np
import math as mt
import matplotlib.pyplot as plt
from scipy import interpolate

# Coordinates of the parallelepiped
xw = 1500
yw = 1500
st = 2500
offset = 800
PARALLELEPIPED_COORDINATES = np.array([[0, 0, 0, 1], [st, 0, 0, 1], [st + offset, st, 0, 1], [0 + offset, st, 0, 1],
                  [0, 0, st, 1], [st, 0, st, 1], [st + offset, st, st, 1], [0 + offset, st, st, 1]])

# Function to project on xy plane with z=0
def project_xy(Figure):
    f = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)
    print('Projection onto xy plane')
    print(Prxy)
    return Prxy

# Function for shifting coordinates
def shift_xyz(Figure, l, m, n):
    f = np.array([[1, 0, 0, l], [0, 1, 0, m], [0, 0, 1, n], [1, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)
    print('Translation')
    print(Prxy)
    return Prxy

# Function for dimetric projection
def dimetric(Figure, TetaG1, TetaG2):
    TetaR1 = (3/14 * TetaG1) / 180
    TetaR2 = (3/14 * TetaG2) / 180
    f1 = np.array([[mt.cos(TetaR1), 0, -mt.sin(TetaR1), 0], [0, 1, 0, 0],
                   [mt.sin(TetaR1), 0, mt.cos(TetaR1), 1], [0, 0, 0, 0]])
    ft1 = f1.T
    Prxy1 = Figure.dot(ft1)
    f2 = np.array([[1, 0, 0, 0], [0, mt.cos(TetaR2), mt.sin(TetaR2), 0], [0, -mt.sin(TetaR2), mt.cos(TetaR2), 0], [0, 0, 0, 1]])
    ft2 = f2.T
    Prxy2 = Prxy1.dot(ft2)
    print('Dimetric projection')
    print(Prxy2)
    return Prxy2

# Function to create parallelepiped using Bezier curves
def draw_parallelepiped(Prxy):
    Ax, Ay = Prxy[0, 0], Prxy[0, 1]
    Bx, By = Prxy[1, 0], Prxy[1, 1]
    Ix, Iy = Prxy[2, 0], Prxy[2, 1]
    Mx, My = Prxy[3, 0], Prxy[3, 1]
    Dx, Dy = Prxy[4, 0], Prxy[4, 1]
    Cx, Cy = Prxy[5, 0], Prxy[5, 1]
    Fx, Fy = Prxy[6, 0], Prxy[6, 1]
    Ex, Ey = Prxy[7, 0], Prxy[7, 1]

    Prxy = np.array([
        # Bottom face
        [Ax, Ay], [Bx, By], [Cx, Cy], [Dx, Dy], [Ax, Ay],

        # Top face
        [Mx, My], [Ix, Iy], [Fx, Fy], [Ex, Ey], [Mx, My],

        # Back face
        [Ix, Iy], [Bx, By], [Ax, Ay], [Mx, My], [Ix, Iy],

        # Right face
        [Fx, Fy], [Cx, Cy], [Bx, By], [Ix, Iy], [Fx, Fy],

        # Front face
        [Ex, Ey], [Dx, Dy], [Cx, Cy], [Fx, Fy], [Ex, Ey],

        # Left face
        [Mx, My], [Ax, Ay], [Dx, Dy], [Ex, Ey], [Mx, My]
    ])

    # Linear interpolation function
    def interpolate_linear(Prxy):
        # Plotting original data points
        for i in range(len(Prxy)):
            x = Prxy[i, 0]
            y = Prxy[i, 1]
            plt.plot(x, y, 'o', label=f'Point {i + 1}')

        # Interpolating and plotting lines
        for i in range(len(Prxy) - 1):
            x = [Prxy[i, 0], Prxy[i + 1, 0]]
            y = [Prxy[i, 1], Prxy[i + 1, 1]]
            f = interpolate.interp1d(x, y, kind='linear')
            xnew = np.linspace(min(x), max(x), 100)
            plt.plot(xnew, f(xnew), label=f'Line {i + 1}', linestyle='-')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Linear Interpolation')
        plt.grid(True)
        plt.show()

    interpolate_linear(Prxy)


st = 50
TetaG1 = 180
TetaG2 = -90
l = (xw / 2) - st
m = (yw / 2) - st
n = m

# Applying transformations
Prlpd1 = shift_xyz(PARALLELEPIPED_COORDINATES, l, m, n)
Prlpd2 = dimetric(Prlpd1, TetaG1, TetaG2)
Prxy3 = project_xy(Prlpd2)
draw_parallelepiped(Prxy3)
