The DCEL data structure is designed to store and manipulate planar subdivisions, such as polygons and polyhedra.
If you want to use DCEL for a voxel-based representation, you need to first convert your voxel data into a mesh or 
surface representation. One approach to convert voxel data to a surface is by using the marching cubes algorithm.

Once you have a surface mesh representation, you can build a DCEL data structure to store the mesh topology 
and perform operations such as edge flips, vertex insertion, and triangulation. The basic steps to use DCEL on a 
voxel are:

1. Convert the voxel data to a surface mesh representation using the marching cubes algorithm.
2. Build a DCEL data structure to store the mesh topology.
3. Traverse the mesh to build the DCEL data structure, using the mesh vertices as DCEL vertices, mesh edges as DCEL half-edges, and mesh faces as DCEL faces.
4. Perform operations on the DCEL, such as inserting vertices or flipping edges, as required by your application.

