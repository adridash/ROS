#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from kobuki_msgs.msg import Sound
from kobuki_msgs.msg import Led


class SoundDistFeedback:
        def __init__(self):
                self.cmd_sound = rospy.Publisher('mobile_base/commands/sound', Sound, queue_size=10)
                self.cmd_led = rospy.Publisher('mobile_base/commands/led1', Led, queue_size=10)
                self.min_sub = rospy.Subscriber('/min_dist', Float32, self.publish_sound)  
                self.r = 1
                self.toggle =True

        # BEGIN MEASUREMENT 
        def publish_sound(self, msg): 
                print (msg.data)
                if(msg.data < 0.5):
                        self.r = rospy.Rate(10)
                        self.led_toggle()
                elif(msg.data < 1):
                        self.r = rospy.Rate(6)
                        self.led_toggle()
                elif(msg.data < 1.3):
                        self.r = rospy.Rate(3)
                        self.led_toggle()
                elif(msg.data < 1.5):
                        self.r = rospy.Rate(1)
                        self.led_toggle()
        
        def led_toggle(self):
                self.toggle = not self.toggle
                
        #END MEASUREMENT
                

        def detection(self):
                print("Starting..")

                # initiliaze
                rospy.init_node('sound_min_dist_feedback', anonymous=False)

                # tell user how to stop TurtleBot
                rospy.loginfo("To stop TurtleBot min_dist_detection CTRL + C")

                # What function to call when you ctrl + c    
                rospy.on_shutdown(self.shutdown)
                # Create a publisher which can "talk" to TurtleBot and tell it to move

                #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
                self.r = rospy.Rate(1)
                # as long as you haven't ctrl + c keeping doing...

                while not rospy.is_shutdown():
                # wait for 1 seconds (1 HZ)
                        self.cmd_sound.publish(3) #valeur du son
                        self.cmd_led.publish(self.toggle) #valeur du son
                        self.r.sleep()




        def shutdown(self):
                # stop turtlebot
                rospy.loginfo("Stop TurtleBot")
                # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
                rospy.sleep(1)




if __name__ == '__main__':
    try:
        c = SoundDistFeedback()
        c.detection()
        #rospy.spin()
    except rospy.ServiceException as exc:
      rospy.loginfo("GoForward node terminated.")
      print("Service did not process request: " + str(exc))

