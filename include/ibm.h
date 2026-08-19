#ifndef IBM_H
#define IBM_H

#include <Eigen/Core>
#include <Eigen/Sparse>


Eigen::MatrixXd IBM_forces(
    const Eigen::MatrixXd& V0,
    const Eigen::MatrixXi& F0,
    const Eigen::MatrixXd& V
);

Eigen::VectorXd IBM_fd_tube_arc(
    const Eigen::MatrixXd& V,
    const Eigen::MatrixXd& Force,
    const Eigen::SparseMatrix<double>& M
);

#endif