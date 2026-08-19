import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import meshzoo 

''' Plot a mesh given V and F'''
def read_obj(filename):
    vertices = []
    faces = []
    i=1
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("v "):
                parts = line.strip().split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])

            elif line.startswith("f "):
                parts = line.strip().split()[1:]

                # Handles faces like:
                # f 1 2 3
                # f 1/1/1 2/2/2 3/3/3
                face = []
                for p in parts:
                    idx = p.split("/")[0] # the index of neighbor vertex
                    face.append(int(idx) - 1)  # OBJ starts at 1, first row = header

                if len(face) == 3:
                    faces.append(face)

    return np.array(vertices), np.array(faces)

V, F = read_obj("data/meshes/arcs/exag_arc.obj")

triangles = V[F]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

mesh = Poly3DCollection(
    triangles,
    facecolor="#8FC5CC",  # triangle fill
    edgecolor="#205B66",  # mesh lines
    linewidth=0.4,
    alpha=1
)
ax.add_collection3d(mesh)

ax.set_xlim(V[:, 0].min(), V[:, 0].max())
ax.set_ylim(V[:, 1].min(), V[:, 1].max())
ax.set_ylim(V[:, 2].min(), V[:, 2].max())
#ax.set_zlim(-1,1) # use this for plane

ax.set_box_aspect([
    np.ptp(V[:, 0]),
    np.ptp(V[:, 1]),
    np.ptp(V[:, 1]) # adjust this if plane
])

# Remove axes, ticks, labels, grid and 3D panes
ax.set_axis_off()

# Background colour
fig.patch.set_facecolor("#dfefef")
ax.set_facecolor("#dfefef")

plt.show()