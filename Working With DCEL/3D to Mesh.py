from skimage import measure
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os


X = []
Y = []
Z = []
if not os.getcwd() == './Res':
    os.chdir('./Res')
with open('ploted.txt') as f:
    for line in f:
        x1, y1, z1= line.split()
        X.append(int(x1))
        Y.append(int(y1))
        Z.append(int(z1))
r=40
# generate a 3D numpy array of voxel data
voxels = np.zeros((r, r, r), dtype=bool)
for i in range(len(X)):
    X[i]=X[i]+int(r/2)
    Y[i]=Y[i]+int(r/2)
    Z[i]=Z[i]+int(r/2)
    voxels[X[i]][Y[i]][Z[i]]=1

# generate the surface mesh using marching cubes algorithm
verts, faces, _, _ = measure.marching_cubes(voxels, level=0.5)


# Convert the vertices and faces to lists
vertices = verts.tolist()
face_indices = faces.tolist()
# Convert the edges to lists
edges = []
for i in range(len(face_indices)):
    edges.append([face_indices[i][0], face_indices[i][1]])
    edges.append([face_indices[i][1], face_indices[i][2]])
    edges.append([face_indices[i][2], face_indices[i][0]])



# Store the vertices, edge and face in DCEL data structure
class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.incident_edge = None
        self.next = None
        self.prev = None
        self.twin = None
        self.face = None

class Edge:
    def __init__(self):
        self.origin = None
        self.twin = None
        self.next = None
        self.prev = None
        self.face = None
    
class Face:
    def __init__(self):
        self.edge = None

class DCEL:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.faces = []

    def add_vertex(self, x, y, z):
        v = Vertex(x, y, z)
        self.vertices.append(v)
        return v

    def add_edge(self):
        e = Edge()
        self.edges.append(e)
        return e

    def add_face(self):
        f = Face()
        self.faces.append(f)
        return f
    

dcel = DCEL()

# Add vertices
for i in range(len(vertices)):
    dcel.add_vertex(vertices[i][0], vertices[i][1], vertices[i][2])

# Add edges
for i in range(len(edges)):
    dcel.add_edge()

# Add faces
for i in range(len(face_indices)):
    dcel.add_face()

#plot the mesh
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:,1], faces, verts[:, 2], cmap='Spectral', lw=1)
plt.show()


