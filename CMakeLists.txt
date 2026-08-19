cmake_minimum_required(VERSION 3.16)

project(discrete_bending_models)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(libigl CONFIG REQUIRED)

# Shared FDHE and IBM functions
add_library(
        bending_models
        src/fdhe.cpp
        src/ibm.cpp
)

target_include_directories(
        bending_models
        PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(
        bending_models
        PUBLIC
        igl::core
)

# Automatically find every experiment file
file(
        GLOB EXPERIMENT_SOURCES
        CONFIGURE_DEPENDS
        "${CMAKE_CURRENT_SOURCE_DIR}/experiments/*.cpp"
)


# Create a separate executable for each experiment
foreach(experiment_source ${EXPERIMENT_SOURCES})

    get_filename_component(
            experiment_name
            ${experiment_source}
            NAME_WE
    )

    add_executable(
            ${experiment_name}
            ${experiment_source}
    )

    target_link_libraries(
            ${experiment_name}
            PRIVATE
            bending_models
    )

    target_compile_definitions(
            ${experiment_name}
            PRIVATE
            PROJECT_DIR="${CMAKE_CURRENT_SOURCE_DIR}"
    )

endforeach()