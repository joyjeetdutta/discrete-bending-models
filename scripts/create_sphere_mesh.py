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

sphere_ns = [6, 8, 12, 18, 24, 32, 40, 48]

for n in sphere_ns:
    V, F = meshzoo.icosa_sphere(n)
    #print(np.pi/V.size)
    write_obj(V, F, f"data/meshes/spheres/sphere{n}.obj")
