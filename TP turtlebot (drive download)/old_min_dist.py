#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan

class MinDistDetect:
        def __init__(self):
                self.min_dist = rospy.Publisher('/min_dist', String, queue_size=10)
                self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)  
                self.min =999

        # BEGIN MEASUREMENT 
        def scan_callback(self, msg): 
                #range_center = msg.ranges[len(msg.ranges)/2] 
                #range_left = msg.ranges[len(msg.ranges)-1] 
                range_right = msg.ranges[0] 
                self.min=999
                for i in range(len(msg.ranges)-1):
                        value = msg.ranges[i]
                        if (value < 0 or value >10):
                                #print("nan", end= "\r")
                                print "nan"
                        elif value < self.min:
                                self.min=value
                #print ("range ahead: left -%0.1f" %range_left, " center-%0.1f" %range_center, " right -%0.1f" %range_right)
                #print ("minimal value = " + str(min), end= "\r")
                print ("minimal value = -%0.2f" %self.min)
                self.min_dist.publish(str(self.min))
        #END MEASUREMENT
                

        def detection(self):
                print("Starting..")

                # initiliaze
                rospy.init_node('min_dist_detection', anonymous=False)

                # tell user how to stop TurtleBot
                rospy.loginfo("To stop TurtleBot min_dist_detection CTRL + C")

                # What function to call when you ctrl + c    
                rospy.on_shutdown(self.shutdown)
                # Create a publisher which can "talk" to TurtleBot and tell it to move

                #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
                r = rospy.Rate(1)
                # as long as you haven't ctrl + c keeping doing...

                while not rospy.is_shutdown():
                # wait for 1 seconds (1 HZ)
                        r.sleep()




        def shutdown(self):
                # stop turtlebot
                rospy.loginfo("Stop TurtleBot")
                # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
                rospy.sleep(1)




if __name__ == '__main__':
    try:
        c = MinDistDetect()
        c.detection()
        #rospy.spin()
    except rospy.ServiceException as exc:
      rospy.loginfo("GoForward node terminated.")
      print("Service did not process request: " + str(exc))

