#include "fdhe.h"
#include <igl/hessian_energy.h>

using namespace Eigen;

const double kappa_b = 1.0;

/**
 * @brief  Calculate curvature bending force using FDHE method
 *
 * Calculate the curvature based bending force of a flat domain using the FDHE method.
 *
 * @param  V_plane:  Matrix with coordinates of each vertex
 * @param  F_plane:  Face-connectivity matrix using Libigl formatting
 * @param        u:  Height field scalar values at each vertex
 *
 * @return Force in the vertical direction at each vertex
 */
VectorXd FDHE_forces(
    const MatrixXd& V_plane,
    const MatrixXi& F_plane,
    const VectorXd& u)
{
    SparseMatrix<double> Q;

    igl::hessian_energy(V_plane, F_plane, Q);

    return -kappa_b * Q * u;
}

/**
 * @brief  Calculate curvature bending force density using FDHE method
 *
 * Calculate the curvature based bending force density of a flat domain using the FDHE method.
 *
 * @param  force_z:  Vertical forces at each vertex
 * @param        M:  Lumped mass matrix of mesh
 *
 * @return Force density in the vertical direction at each vertex
 */
VectorXd FDHE_fd(
    const VectorXd& force_z,
    const SparseMatrix<double>& M)
{
    VectorXd f_d(force_z.size());

    for (int i = 0; i < force_z.size(); ++i) {
        // Voronoi area associated with vertex i
        f_d(i) = force_z(i) / M.coeff(i, i);
    }

    return f_d;
}