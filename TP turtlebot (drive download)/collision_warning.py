#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import Sound
from geometry_msgs.msg import Twist
cmd_sound = rospy.Publisher('mobile_base/commands/sound', Sound, queue_size=10)
def processBump(data):
            global bump
   	    
            if (data.state == BumperEvent.PRESSED):
                bump = True

		rospy.loginfo("Bumper Enfonce !")
 		cmd_sound.publish(0)
            else:
                bump = False
            #rospy.loginfo(data.bumper)

def GoForward():
        print("Starting..")

        # initiliaze
        rospy.init_node('GoForward', anonymous=False)

        # tell user how to stop TurtleBot
        rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c    
        rospy.on_shutdown(shutdown)
        # Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        sub = rospy.Subscriber('mobile_base/events/bumper', BumperEvent, processBump)
        #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);

        # Twist is a datatype for velocity
        move_cmd = Twist()
        # let's go forward at 0.2 m/s
        #move_cmd.linear.x = 0.2
        # let's turn at 0 radians/s
        move_cmd.angular.z = 0.0
        # as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
            # publish the velocity
            cmd_vel.publish(move_cmd)
            # wait for 0.1 seconds (10 HZ) and publish again
            r.sleep()




def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        cmd_vel.publish(Twist())
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)




if __name__ == '__main__':
    try:
        GoForward()
    except rospy.ServiceException as exc:
      rospy.loginfo("GoForward node terminated.")
      print("Service did not process request: " + str(exc))

