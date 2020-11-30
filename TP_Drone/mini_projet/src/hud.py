#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
import cv2 #opencv
from cv_bridge import CvBridge  #converts between ROS Image messages and OpenCV images.
#from visualization_msgs.msg import Marker


class hud :

	def __init__(self):
		rospy.init_node('hud', anonymous=True)
		rospy.Subscriber('/bebop/image_raw', Image, self.callbackImg)
		rospy.Subscriber('/altitude', Float32, self.callbackAltitude)
		#rospy.Subscriber('/visualisation_marker', Marker, self.callbackAltitude)
		self.pub_hud = rospy.Publisher('/bebop/hud', Image, queue_size=10)
		self.bridge = CvBridge()
		self.altitude = 0

		# What function to call when you ctrl + c    
		rospy.loginfo("To stop control node CTRL + C or CTRL MAJ C")
		rospy.on_shutdown(self.shutdown)

	def callbackImg(self,msg) :
	
		try:		
			img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
			
			txt = str(self.altitude) #convertion de l'altitude en texte
			emplacement = (0,0)
			font = cv2.FONT_HERSHEY_SIMPLEX
			fontScale = 1
			thickness = 2
			color = (0,0,0) #noir => attention ici BGR
			cv2.PutText(img, txt, emplacement, font, fontScale, color, thickness, cv2.LINE_AA)
			img_hud = self.ridge.cv2_to_imgmsg(img, encoding="passthrough") #convertion opencv to ros
			self.pub_hud.publish(img_hud) #publication de l'image
		
		except CvBridgeError as e:
			print(e)
			
	def callbackAltitude(self,msg) :
		self.altitude = msg

	def shutdown(self):
			# stop node
			rospy.loginfo("Stop Control node")

if __name__ == '__main__' :
	try :
		hud = hud()
		rospy.spin()
	except rospy.ServiceException as exc:
		rospy.loginfo("control node terminated.")
		print("Service did not process request: " + str(exc))
