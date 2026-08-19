#include "fdhe.h"
#include "ibm.h"

#include <igl/massmatrix.h>
#include <igl/read_triangle_mesh.h>

#include <Eigen/Core>
#include <Eigen/Sparse>

#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace Eigen;
using namespace std;

/**
 * @brief  Save a vector to a CSV file
 *
 * @param output_filename:  Path to the output file
 * @param   vector_to_save:  Values to save
 */
void save_file(
    const string& output_filename,
    const VectorXd& vector_to_save)
{
    ofstream file(output_filename);

    file << scientific << setprecision(40);
    file << "index,force_density\n";

    for (int i = 0; i < vector_to_save.size(); ++i) {
        file << i << ","
             << vector_to_save(i)
             << "\n";
    }
}

int main()
{
    vector<int> ntheta_values =
        {6, 8, 12, 18, 24, 32, 40, 48};

    const double R = 100.0;

    for (int ntheta : ntheta_values) {

        cout << "Processing ntheta = "
             << ntheta << endl;

        string plane = string(PROJECT_DIR) +
            "/Poster_data/meshes/planes/p_ntheta" + to_string(ntheta) + ".obj";

        string tube_arc =
            string(PROJECT_DIR) + "/Poster_data/meshes/arcs/ntheta" + to_string(ntheta) + ".obj";

        MatrixXd V_plane;
        MatrixXi F_plane;
        igl::read_triangle_mesh(plane, V_plane, F_plane);

        MatrixXd V_arc;
        MatrixXi F_arc;
        igl::read_triangle_mesh(tube_arc, V_arc, F_arc);

        // Voronoi mass matrix of the deformed arc
        SparseMatrix<double> M_v;

        igl::massmatrix(
            V_arc,
            F_arc,
            igl::MASSMATRIX_TYPE_VORONOI,
            M_v
        );

        // IBM METHOD
        MatrixXd force_ibm =
            IBM_forces(
                V_plane,
                F_plane,
                V_arc
            );

        VectorXd fd_ibm =
            IBM_fd(
                V_arc,
                force_ibm,
                M_v
            );

       // FDHE METHOD
        VectorXd u(V_plane.rows());

        for (int i = 0; i < V_plane.rows(); ++i) {
            const double x = V_plane(i, 0);
            u(i) = R - sqrt(R * R - x * x);
        }

        VectorXd force_fdhe = FDHE_forces(V_plane, F_plane, u);
        VectorXd fd_fdhe = FDHE_fd(force_fdhe, M_v);

        // SAVE RESULTS
        string ibm_output =
            string(PROJECT_DIR) +
            "/Poster_data/ibm/fd/fd_ntheta" +
            to_string(ntheta) +
            ".csv";

        string fdhe_output =
            string(PROJECT_DIR) +
            "/Poster_data/hess/fd/fd_ntheta" +
            to_string(ntheta) +
            ".csv";

        save_file(ibm_output, fd_ibm);
        save_file(fdhe_output, fd_fdhe);
    }

    cout << "Finished all arc resolutions."
         << endl;

    return 0;
}