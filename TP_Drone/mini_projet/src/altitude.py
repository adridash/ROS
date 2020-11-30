#!/usr/bin/env python
import rospy
from bebop_msgs.msg import Ardrone3PilotingStateAltitudeChanged
from std_msgs.msg import Float32


class Altitude:

	def __init__(self):
		#Creation du topic altitude
		self.altitude_pub = rospy.Publisher('/altitude', Float32, queue_size=10)
		self.altitude_sub = rospy.Subscriber('/bebop/states/ardrone3/PilotingState/AltitudeChanged', Ardrone3PilotingStateAltitudeChanged, self.callback)  
		print("Starting..")

		# initiliaze
		rospy.init_node('altitude', anonymous=False)

		# tell user how to stop node
		rospy.loginfo("To stop altitude node CTRL + C")

		# What function to call when you ctrl + c    
		rospy.on_shutdown(self.shutdown)

		r = rospy.Rate(1) #set the rate to 1Hz
                
                
	def callback(self, msg):
		rospy.loginfo(msg.altitude)
		self.altitude_pub.publish(msg.altitude) #publish altitude(float32) on topic /altitude
        

	def shutdown(self):
		rospy.loginfo("Stop Altitude node")
		rospy.sleep(1)

if __name__ == '__main__':
	try:
		c = Altitude()
		rospy.spin()
	except rospy.ServiceException as exc:
		rospy.loginfo("Altitude node terminated.")
		print("Service did not process request: " + str(exc))
