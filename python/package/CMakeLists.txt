cmake_minimum_required(VERSION 3.5)
project(bindings)

# find_package(PCL REQUIRED)
find_package(PCL COMPONENTS common REQUIRED)
find_package(pybind11)

# get the parent directory
get_filename_component(PYTHON_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} DIRECTORY)

# variable for holding folder name which contains pybind11 generated files
set(PYBIND11_GEN pybind11-gen)

# recursively get all pybind11 generated files
file(GLOB_RECURSE PYBIND11_FILES ${PYTHON_DIRECTORY}/${PYBIND11_GEN}/*.cpp)

# add all pybind11 files to `pcl` module in python
foreach(PYBIND11_FILE ${PYBIND11_FILES})
	pybind11_add_module(pcl ${PYBIND11_FILE})
endforeach()

target_link_libraries(pcl PRIVATE ${PCL_LIBRARIES})
# add_dependencies(pcl_demo some_other_target)
