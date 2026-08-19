#ifndef FDHE_H
#define FDHE_H

#include <Eigen/Core>
#include <Eigen/Sparse>


Eigen::VectorXd FDHE_forces(
    const Eigen::MatrixXd& V_plane,
    const Eigen::MatrixXi& F_plane,
    const Eigen::VectorXd& u
);

Eigen::VectorXd FDHE_fd(
    const Eigen::VectorXd& force_z,
    const Eigen::SparseMatrix<double>& M
);

#endif