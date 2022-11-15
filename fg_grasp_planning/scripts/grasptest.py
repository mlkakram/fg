#!/usr/bin/env python3

import roslib.packages
import sys
pkg_name = 'graspit_commander'
sys.path.insert(0,roslib.packages.get_pkg_dir(pkg_name)+'/src/' + pkg_name)

from graspit_commander import GraspitCommander as gc
from graspit_interface.msg import SearchSpace 
from geometry_msgs.msg import Pose 
from graspit_interface.srv import SetRobotPose
from graspit_interface.msg import *



# World setting 
gc.clearWorld()
gc.loadWorld("ShlMug")
searchtype = SearchSpace()

# Initiating the grasp planning and also specifying the search space and enclosing on the object after the search is done 
searchtype.type = 0
gc.planGrasps(search_energy="CONTACT_ENERGY",max_steps=50000,search_space=searchtype)
gc.autoGrasp()

