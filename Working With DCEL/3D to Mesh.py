from skimage import measure
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
import sqlite3
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
    
    def hsort(self, e1, e2):
        """Sort two half-edges by their origin vertex"""
        if e1.origin.x < e2.origin.x:
            return -1
        elif e1.origin.x > e2.origin.x:
            return 1
        elif e1.origin.y < e2.origin.y:
            return -1
        elif e1.origin.y > e2.origin.y:
            return 1
        elif e1.origin.z < e2.origin.z:
            return -1
        elif e1.origin.z > e2.origin.z:
            return 1
        else:
            return 0
        
    def check_edge(self, v1, v2):
        """Check if an edge exists between two vertices"""
        for e in self.edges:
            if e.origin == v1 and e.twin.origin == v2:
                return e
        return None
    
    def aread(self, v1, v2, v3):
        """Calculate the area of the triangle formed by three vertices"""
        return 0.5 * np.linalg.norm(np.cross(v2 - v1, v3 - v1))
    
    def build(self):
        """Build the DCEL data structure"""
        # Add edges
        for i in range(len(edges)):
            e = self.add_edge()
            e.origin = self.vertices[edges[i][0]]
            e.twin = self.add_edge()
            e.twin.origin = self.vertices[edges[i][1]]
            e.twin.twin = e
            e.twin.face = self.faces[0]
            e.face = self.faces[0]
        
        # Sort the edges
        self.edges.sort(key=lambda e: e.origin)
        
        # Add next and prev pointers
        for i in range(len(self.edges)):
            self.edges[i].next = self.edges[(i + 1) % len(self.edges)]
            self.edges[i].prev = self.edges[(i - 1) % len(self.edges)]
        
        # Add incident edge pointers
        for v in self.vertices:
            v.incident_edge = self.edges[0]
            for e in self.edges:
                if e.origin == v:
                    v.incident_edge = e
                    break
        
        # Add twin pointers
        for e in self.edges:
            if e.twin is None:
                e.twin = self.check_edge(e.twin.origin, e.origin)
                e.twin.twin = e
        
        # Add face pointers
        for e in self.edges:
            if e.face is None:
                e.face = self.add_face()
                e.face.edge = e
                e.twin.face = e.face
        
        # Add next and prev pointers for the faces
        for f in self.faces:
            e = f.edge
            while True:
                e.next = e.twin.next
                e.next.prev = e
                e = e.next
                if e == f.edge:
                    break

dcel = DCEL()
# use the build function to build the DCEL data structure
# dcel.build()

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


# Store the vertices, edge and face in a SQLite database
conn = sqlite3.connect('mesh.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE vertices
                (id integer, x real, y real, z real)''')
c.execute('''CREATE TABLE edges
                (id integer, origin integer, twin integer, next integer, prev integer, face integer)''')    
c.execute('''CREATE TABLE faces
                (id integer, edge integer)''')  

# Insert a row of data
for i in range(len(vertices)):
    c.execute("INSERT INTO vertices VALUES (?, ?, ?, ?)", (i, vertices[i][0], vertices[i][1], vertices[i][2]))
for i in range(len(edges)):
    c.execute("INSERT INTO edges VALUES (?, ?, ?, ?, ?, ?)", (i, edges[i][0], edges[i][1], 0, 0, 0))
for i in range(len(face_indices)):
    c.execute("INSERT INTO faces VALUES (?, ?)", (i, 0))

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

# Close the connection
conn.close()

