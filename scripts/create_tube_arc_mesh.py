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

def tube_arc(length=5.0, radius=10.0, n_theta=30, theta_min=0.0, theta_max=np.pi):
    """
    Create tube arc

    length: tube length along z
    radius: circle radius in xy plane
    n_theta: number of samples around the arc
    theta_min, theta_max: angular span in radians
    """

    # Arc length = radius * angle
    arc_length = radius * abs(theta_max - theta_min)

    # Choose z divisions so triangles/quads are not too stretched
    n_y = max(
        2,
        int(round(length * (n_theta - 1) / arc_length)) + 1)
    
    theta_range = np.linspace(theta_min, theta_max, num=n_theta)
    y_range = np.linspace(-0.5 * length, 0.5 * length, num=n_y)

    # Store all (theta, y) coordinates
    proto_nodes = np.dstack(
        np.meshgrid(theta_range, y_range, indexing="ij")
    ).reshape(-1, 2)

    # Tube axis along y; circular arc in the xz-plane
    vertices = np.column_stack([
        -radius * np.cos(proto_nodes[:, 0]),  # x
        proto_nodes[:, 1],                    # y
        radius * np.sin(proto_nodes[:, 0]),   # z
    ])

    faces = []
    
    # store the face connections. 
    for i in range(n_theta - 1):
        for j in range(n_y - 1):
            # n_y is how many points along z-axis per theta row
            # so first we take two values of z with one spacing, along the length of the arc, then we move up to the next angle and take two points 
            # this creates the angled rectangle
            # this angled rectangle is split in half for triangulation. 
            
            a = i * n_y + j
            b = (i + 1) * n_y + j
            c = (i + 1) * n_y + j + 1
            d = i * n_y + j + 1

            faces.append([a, c, d])
            faces.append([a, b, c])

    return vertices, np.array(faces)

def plane(length=5.0, radius=10.0, n_width=30,
          theta_min=0.0, theta_max=np.pi):

    width = radius * abs(theta_max - theta_min)
    n_y = max(
        2,
        int(round(length * (n_width - 1) / width)) + 1)


    x_range = np.linspace(-0.5 * width, 0.5 * width, num=n_width)
    y_range = np.linspace(-0.5 * length, 0.5 * length, num=n_y)

    proto_nodes = np.dstack(
        np.meshgrid(x_range, y_range, indexing="ij")
    ).reshape(-1, 2)

    # Flat plane in xy plane, with z = 0
    vertices = np.column_stack([
        proto_nodes[:, 0],
        proto_nodes[:, 1],
        np.zeros(len(proto_nodes)),
    ])

    faces = []

    for i in range(n_width - 1):
        for j in range(n_y - 1):
            a = i * n_y + j
            b = (i + 1) * n_y + j
            c = (i + 1) * n_y + j + 1
            d = i * n_y + j + 1

            faces.append([a, c, d])
            faces.append([a, b, c])

    return vertices, np.array(faces)

radius = 1.0     # large radius = gentle curve
length = 100.0
n_theta = 48 # change
theta_min=np.radians(88)
theta_max=np.radians(92)

V, F = tube_arc(
        0.8,
        0.5,
        18,
        np.radians(60),
        np.radians(130)
    )


V_plane, F_plane = plane(
    0.8,
    0.5,
    40,
    np.radians(60),
    np.radians(130)
)


#write_obj(V, F, f"Poster_data/meshes/arcs/exag_arc.obj")
write_obj(V_plane, F_plane, "Poster_data/meshes/planes/model_plane.obj")
