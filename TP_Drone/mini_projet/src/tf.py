#!/usr/bin/env python

import rospy

from nav_msgs.msg import Odometry
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker

class tf : 

	def __init__ (self) :

		rospy.init_node('tf', anonymous=True) #init de la node
		rospy.Subscriber('/bebop/odom', Odometry, self.callback) #subsciber pour l'odometrie
		self.vizu = rospy.Publisher('/visualisation_marker', Marker, queue_size=0) #publisher a creer
		self.id = 0
		# What function to call when you ctrl + c    
		rospy.loginfo("To stop control node CTRL + C")
		rospy.on_shutdown(self.shutdown)
		
	# Fonction declenchee par le Subscriber 
	def callback(self,msg) :

		marker = Marker()
		marker.header.frame_id = "/base_link"
		marker.id = self.id
		marker.type = marker.CUBE #le type peut etre CUBE ou SPHERE ou autre
		marker.action = marker.ADD #on ajoute le marker (on pourrait le supprimer)
		marker.scale.x = 0.2
		marker.scale.y = 0.2
		marker.scale.z = 0.2
		marker.color=ColorRGBA(0, 1, 0, 1) #couleur du marker
		marker.pose.orientation.w = 1.0
		marker.pose.position.x = msg.pose.pose.position.x #position du marker définie selon la position 
		marker.pose.position.y = msg.pose.pose.position.y #du drone, en x, y et z
		marker.pose.position.z = msg.pose.pose.position.z
		self.id += 1
		self.vizu.publish(marker)

		print(msg.pose.pose.position)

	def shutdown(self):
		# stop node
		rospy.loginfo("Stop Control node")

if __name__ == '__main__' :
    try :
        tf = tf()
        rospy.spin()
    except rospy.ServiceException as exc:
      	rospy.loginfo("control node terminated.")
      	print("Service did not process request: " + str(exc))
