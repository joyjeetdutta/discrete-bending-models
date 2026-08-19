import meshzoo
import numpy as np 

def write_obj(vertices, faces, output_obj_path="Meshes/output.obj"):
    with open(output_obj_path, "w") as obj_file:

        # Write vertices
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        # Write faces
        # OBJ indices start at 1, but Python indices start at 0
        for face in faces:
            obj_file.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")

#sphere_ns = [3,5,10,20,30]
sphere_ns = [6, 8, 12, 18, 24, 32, 40, 48]

for n in sphere_ns:
    V, F = meshzoo.icosa_sphere(n)
    #print(np.pi/V.size)
    write_obj(V, F, f"Poster_data/meshes/spheres/sphere{n}.obj")

#V, F = meshzoo.icosa_sphere(5)
#write_obj(V,F, f"Meshes/sphere_lowres.obj")

'''
points2d, cells = meshzoo.rectangle_quad(
    np.linspace(0.0, 1.0, 5),
    np.linspace(0.0, 1.0, 5),
    cell_type="quad4",  # or "quad8", "quad9"
)

points3d = np.column_stack([
    points2d[:, 0],
    points2d[:, 1],
    np.zeros(len(points2d)),
])

write_obj(points3d,cells, f"Meshes/stretched_plane.obj")
'''

#radius=1
#length = 75.0

#V, F = meshzoo.tube(length, radius, n=300)

#print("resolution: ")
#print(np.sqrt(2*np.pi*radius*length*(1/V.shape[0])))
        
#write_obj(V,F, f"Tube/tube_meshes/tube_r1_highres.obj")

