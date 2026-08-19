#include "ibm.h"

#include <igl/read_triangle_mesh.h>

#include <Eigen/Core>

#include <fstream>
#include <iostream>
#include <string>
#include <vector>


using namespace Eigen;


void save_file(
    const std::string& filename,
    const VectorXd& values)
{
    std::ofstream file(filename);

    for (int i = 0; i < values.size(); ++i) {
        file << values(i) << "\n";
    }
}


int main()
{
    const std::vector<int> ntheta_values =
    {6, 8, 12, 18, 24, 32, 40, 48};

    for (int ntheta : ntheta_values)
    {
        std::cout
            << "Processing sphere"
            << ntheta
            << std::endl;

        const std::string sphere =
            std::string(PROJECT_DIR) +
            "/data/meshes/spheres/sphere" +
            std::to_string(ntheta) +
            ".obj";

        // Load sphere mesh
        MatrixXd V_sphere;
        MatrixXi F_sphere;

        if (!igl::read_triangle_mesh(
                sphere,
                V_sphere,
                F_sphere))
        {
            std::cerr
                << "Could not load sphere"
                << ntheta
                << std::endl;

            continue;
        }

        // Calculate mean curvature
        VectorXd mean_curv =
            cot_curv(V_sphere, F_sphere);

        const std::string curv_output =
            std::string(PROJECT_DIR) +
            "/data/results/ibm/curv/sphere/curv_s" +
            std::to_string(ntheta) +
            ".csv";

        // Save curvature values
        save_file(curv_output, mean_curv);
    }

    std::cout
        << "Finished all sphere resolutions."
        << std::endl;

    return 0;
}