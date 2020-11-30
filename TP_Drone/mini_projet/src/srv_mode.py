#!/usr/bin/env python

import sys
import rospy
from mini_projet.srv import Booleen

def surveillance(req):
    #return True boolean if mode surveillance is called
    return True

def loisir(req):
    #return false boolean if mode loisir is called
    return False

def add_two_ints_server():
    rospy.init_node('ModeSurv')
    rospy.Service('Surveillance', Booleen, surveillance)
    rospy.Service('Loisir', Booleen, loisir)
    
    rospy.spin()

if __name__ == "__main__":
    print("Serveur launched")
    add_two_ints_server()