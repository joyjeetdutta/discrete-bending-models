#include "ibm.h"

#include <igl/cotmatrix.h>
#include <igl/invert_diag.h>
#include <igl/massmatrix.h>

#include <cmath>

using namespace Eigen;

const kappa_b = 1;


/**
 * @brief  Calculate the mean curvature using the cotangent Laplacian
 *
 * Calculate the mean curvature magnitude at each vertex using the cotangent Laplacian and Voronoi mass matrix.
 *
 * @param V:  Vertex positions of the mesh
 * @param F:  Triangular faces of the mesh
 *
 * @return Mean curvature magnitude at each vertex
 */
VectorXd cot_curv(
    const MatrixXd& V,
    const MatrixXi& F)
{
    SparseMatrix<double> L;
    SparseMatrix<double> Minv;

    igl::cotmatrix(V, F, L);

    SparseMatrix<double> M = mass_matrix(V, F);

    igl::invert_diag(M, Minv);

    MatrixXd Hn_pointwise = Minv * L * V;

    VectorXd H =
        0.5 * Hn_pointwise.rowwise().norm();

    return H;
}

/**
 * @brief  Calculate curvature bending forces using the IBM method
 *
 * Construct the IBM bending operator from the reference mesh and apply it to the current vertex positions.
 *
 * @param V0:  Vertex positions of the reference mesh
 * @param F0:  Triangular faces of the reference mesh
 * @param  V:  Current vertex positions of the mesh
 *
 * @return Bending force vector at each vertex
 */
MatrixXd IBM_forces(
    const MatrixXd& V0,
    const MatrixXi& F0,
    const MatrixXd& V)
{
    SparseMatrix<double> L;
    SparseMatrix<double> M;
    SparseMatrix<double> Minv;

    igl::cotmatrix(V0, F0, L);

    igl::massmatrix(
        V0,
        F0,
        igl::MASSMATRIX_TYPE_VORONOI,
        M
    );

    igl::invert_diag(M, Minv);

    SparseMatrix<double> Q =
        L.transpose() * Minv * L;

    return -kappa_b * Q * V;
}

/**
 * @brief  Calculate normal force density for the tube arc test case
 *
 * Project the IBM bending force onto the radial surface normal and divide by the associated vertex area.
 *
 * @param     V:  Vertex positions of the tube arc mesh
 * @param Force:  Bending force vector at each vertex
 * @param     M:  Lumped mass matrix of the mesh
 *
 * @return Normal force density at each vertex
 */
VectorXd IBM_fd_tube_arc(
    const MatrixXd& V,
    const MatrixXd& Force,
    const SparseMatrix<double>& M)
{
    VectorXd f_d(V.rows());

    for (int i = 0; i < V.rows(); ++i) {
        const double x = V(i, 0);
        const double z = V(i, 2);
        const double r = std::sqrt(x * x + z * z);

        if (r < 1e-12) {
            f_d(i) = 0.0;
            continue;
        }

        // Radial normal for your tube/arc test case
        VectorXd n_i(3);
        n_i(0) = x / r;
        n_i(1) = 0.0;
        n_i(2) = z / r;

        // Convert normal nodal force into normal force density
        f_d(i) =
            Force.row(i).dot(n_i) / M.coeff(i, i);
    }

    return f_d;
}