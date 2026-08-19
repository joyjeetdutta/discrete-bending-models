import numpy as np
import matplotlib.pyplot as plt
import csv

R = 100.0
H_exact = 1
#H_exact = 1.0 / (2.0 * R)
#fd_exact = 1/(R**3)

ntheta_values = [6, 8, 12, 18, 24, 32, 40, 48]

# Remove two vertex layers from every boundary
boundary_layers = 2

n_points = []
n_interior_points = []
mean_abs_error = []
mean_curvature = []


for ntheta in ntheta_values:
    filename = f"data/ibm/curv/curv_s{ntheta}.csv"

    indices = []
    curvatures = []

    # Load every vertex before filtering
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip "index,H"

        for row in reader:
            indices.append(int(row[0]))
            curvatures.append(float(row[1]))

    indices = np.array(indices, dtype=int)
    curvatures = np.array(curvatures, dtype=float)

    total_points = len(curvatures)

    # Number of rows in the arc direction
    n_s = ntheta

    if total_points % n_s != 0:
        raise ValueError(
            f"For ntheta={ntheta}, the number of vertices "
            f"{total_points} is not divisible by ntheta."
        )

    # Number of points along y in each row
    n_y = total_points // n_s

    # For vertex index:
    #
    # index = s_index * n_y + y_index
    #
    # s_index gives the row along the arc.
    # y_index gives the position within that row.
    s_index = indices // n_y
    y_index = indices % n_y

    # Keep only vertices that are at least two layers
    # away from every boundary
    interior_mask = (
        (s_index >= boundary_layers)
        & (s_index < n_s - boundary_layers)
        & (y_index >= boundary_layers)
        & (y_index < n_y - boundary_layers)
    )

    interior_curvatures = curvatures[interior_mask]

    errors = np.abs(interior_curvatures - H_exact)

    n_points.append(total_points)
    n_interior_points.append(interior_curvatures.size)
    mean_curvature.append(np.mean(interior_curvatures))
    mean_abs_error.append(np.mean(errors))

    print(f"ntheta = {ntheta}")
    print(f"  n_s:                  {n_s}")
    print(f"  n_y:                  {n_y}")
    print(f"  Total points:         {total_points}")
    print(f"  Interior points:      {interior_curvatures.size}")
    print(f"  Mean curvature:       {np.mean(interior_curvatures):.16e}")
    print(f"  Exact curvature:      {H_exact:.16e}")
    print(f"  Mean absolute error:  {np.mean(errors):.16e}")
    print()

n_points = np.array(n_points)
mean_abs_error = np.array(mean_abs_error)

plt.plot(
    n_points,
    mean_abs_error,
    "o-"
)

plt.xlabel(r"Number of mesh vertices $N$")
plt.ylabel("Mean absolute force density error")
plt.title("Mean absolute force density error with FDHE for various resolutions of the test case")
plt.grid(True, which="both", alpha=0.3)

plt.show()