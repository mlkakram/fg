#!/usr/bin/env python3

import sys 
import roslib.packages
pkg_name1 = 'graspit_commander'
pkg_name2 = 'grid_sample_client'
sys.path.insert(0,roslib.packages.get_pkg_dir(pkg_name1)+'/src/' + pkg_name1)
sys.path.insert(0,roslib.packages.get_pkg_dir(pkg_name2)+'/src/' + pkg_name2)

import graspit_commander
import grid_sample_client

gc = graspit_commander.GraspitCommander()

# Setting up the world
gc.clearWorld()
gc.loadWorld('ShlMug')

pre_grasps = grid_sample_client.GridSampleClient.computePreGrasps(5)	# resolution, sampling_type

grasps = grid_sample_client.GridSampleClient.simannPreGrasps(pre_grasps.grasps)