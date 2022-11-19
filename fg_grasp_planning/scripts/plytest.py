#!/usr/bin/env python3 

import numpy as np
import trimesh
import skfmm

def sdf(path, ds):
    """signed-distance-function return a grid which is equally spaced in space
    along three directions (x, y and z), and each grid point stores a signed
    scalar value indicating its shortest distance to the particle's interface

    INPUTS:
    path: directory of the .stl file of the CAD model.
    ds: the grid resolution.

    OUTPUTS:
    grid: list of x, y and z points represents the grid that the particle
          exists in.
    sdv: list of signed distance values of every point in the grid (negative
       value -> inside the particle, postive value -> outside  the particle.)
    """
    mesh = trimesh.load(path)
    #voxelize the loaded mesh with voxel size equals to the grid resolution (ds)
    angel_voxel = mesh.voxelized(ds).fill()
    #compure the voxels center points
    voxel_centers = angel_voxel.points

    #constructing the grid
    inc = max(1, ds)
    grid_max_x = max(voxel_centers[:,0]) + inc
    grid_min_x = min(voxel_centers[:,0]) - inc
    grid_max_y = max(voxel_centers[:,1]) + inc
    grid_min_y = min(voxel_centers[:,1]) - inc
    grid_max_z = max(voxel_centers[:,2]) + inc
    grid_min_z = min(voxel_centers[:,2]) - inc

    grid_xlength = ((grid_max_x - grid_min_x)/ds) + 1
    grid_ylength = ((grid_max_y - grid_min_y)/ds) + 1
    grid_zlength = ((grid_max_z - grid_min_z)/ds) + 1

    X, Y, Z = np.meshgrid(np.linspace(grid_min_x, grid_max_x, int(grid_xlength)),
                          np.linspace(grid_min_y, grid_max_y, int(grid_ylength)),
                          np.linspace(grid_min_z, grid_max_z, int(grid_zlength)))

    #prepare the input for skfmm.distance which take an array with the same
    #dimesion of the grid. in the grid, 1 represents the points outside the
    #particle and -1 represents the points inside the particle.
    phi = 1 * np.ones_like(X)
    cpoints = voxel_centers.tolist() #for in operation
    l = [0, 0, 0]
    limits = np.shape(X)

    X = X.flatten()
    Y = Y.flatten()
    Z = Z.flatten()
    grid = np.array([X, Y, Z]).T
    grid = grid.tolist()
    phi = phi.flatten()

    voxel_centers = np.round(voxel_centers, 2)
    grid = np.round(grid, 4)

    for i in range(len(X)):
        if np.any(np.all(grid[i] == voxel_centers, axis=1)):
            phi[i] = -1
    phi = np.reshape(phi, limits)

    #compute the signed distance values and flatten the grid for concatination
    sdf = skfmm.distance(phi, dx=ds)
    sdv = sdf.flatten().tolist()
    sdv = np.round(sdv, 4)

    grid = [X, Y, Z]


    # generate a voxelized mesh from the voxel grid representation, using the calculated colors
    voxelized_mesh = angel_voxel.as_boxes()

    # Initialize a scene
    s = trimesh.Scene()
    # Add the voxelized mesh to the scene. If want to also show the intial mesh uncomment the second line and change the alpha channel of in the loop to something <100
    s.add_geometry(voxelized_mesh)
    s.add_geometry(mesh)
    s.show()

    return grid, sdv, cpoints

if __name__ == "__main__":

    p = "~/Downloads/drill.stl"
    ds = 2
    g = sdf(p, ds)


