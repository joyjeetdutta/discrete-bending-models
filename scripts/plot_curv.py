import numpy as np
import matplotlib.pyplot as plt
import csv


R = 100.0
H_exact = 1

ntheta_values = [6, 8, 12, 18, 24, 32, 40, 48]

n_points = []
n_interior_points = []
mean_abs_error = []
mean_curvature = []
spacings = []


for ntheta in ntheta_values:
    filename = f"data/ibm/curv/sphere/curv_s{ntheta}.csv"

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
    
    errors = np.abs(curvatures - H_exact)

    n_points.append(total_points)
    spacings.append(4*np.pi*(1/total_points))
    mean_curvature.append(np.mean(curvatures))
    mean_abs_error.append(np.mean(errors))

    print(f"ntheta = {ntheta}")
    print(f"  Total points:         {total_points}")
    print(f"  Mean curvature:       {np.mean(curvatures):.16e}")
    print(f"  Exact curvature:      {H_exact:.16e}")
    print(f"  Mean absolute error:  {np.mean(errors):.16e}")
    print()

n_points = np.array(n_points)
spacings = np.array(spacings)
mean_abs_error = np.array(mean_abs_error)

p, log_C = np.polyfit(np.log(spacings), np.log(mean_abs_error), 1)
C = np.exp(log_C)

print("Convergence order:", p)


plt.loglog(
    spacings,
    mean_abs_error,
    "o-", 
    color="#5E8E98", 
    markersize=10,
    label="Numerical error"
)

plt.loglog(
    spacings,
    C * spacings**p,
    "--",
    color="black",
    label=rf"Fit: $E \propto a_N^{{{p:.2f}}}$"
)


plt.xlabel(r"Characteristic area per vertex $a_N$")
plt.ylabel("Mean absolute $H$ error")
plt.title("Loglog plot of mean absolute $H$ error for unit sphere meshes using IBM")

plt.gca().set_facecolor("#EEF9FA")
plt.gcf().set_facecolor("#EEF9FA")

plt.grid(True, which="both", alpha=0.3)
plt.legend()


plt.show()