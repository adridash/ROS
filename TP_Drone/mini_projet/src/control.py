#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from mini_projet.srv import Booleen

class Control :

    def __init__(self):       
        print("Starting..")
        self.mode = 0

        # initiliaze
        rospy.init_node('control', anonymous=False)

        # What function to call when you ctrl + c    
        rospy.loginfo("To stop control node CTRL + C")
        rospy.on_shutdown(self.shutdown)
        
        self.decollage_pub = rospy.Publisher('/bebop/takeoff', Empty, queue_size=0)

        self.atterrissage_pub = rospy.Publisher('/bebop/land', Empty, queue_size=0)

        self.reset_pub = rospy.Publisher('/bebop/reset', Empty, queue_size=0)

        self.mouvement_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=0)

        rospy.Subscriber('/joy', Joy, self.callback)  

        self.r = rospy.Rate(10)
               

            
    # Fonction declenchee par le Subscriber 
    def callback(self, msg):
        #3 boutons commun au deux modes
        if(msg.buttons[0] == 1) :
            self.reset_pub.publish()

        if(msg.buttons[1] == 1) :
            self.atterrissage_pub.publish()

        if(msg.buttons[2] == 1) :
            self.decollage_pub.publish() 

        if (msg.buttons[9] == 1): #Mode surveillance
            mode_srv = rospy.ServiceProxy('Surveillance', Booleen)
            self.mode = mode_srv().out

        elif (msg.buttons[8] == 1): #Mode loisir
            mode_srv = rospy.ServiceProxy('Loisir', Booleen)
            self.mode = mode_srv().out

        if (self.mode == 0): #si mode loisir
            var = 0
            
            if(msg.buttons[7] == 1) : #Monter

                var = 1

            if(msg.buttons[6] == 1) : #Descendre

                var = -1
                
            mouvement = Twist()

            mouvement.linear.x = msg.axes[4]  
            mouvement.linear.y = msg.axes[3]
            mouvement.linear.z = var 
            mouvement.angular.x = 0
            mouvement.angular.y = 0 
            mouvement.angular.z = msg.axes[0] 

            self.mouvement_pub.publish(mouvement)
        #sinon on envoi le publish dans le rospy.is_shutdonw  

    def shutdown(self):
        # stop node
        rospy.loginfo("Stop Control node")

if __name__ == '__main__':
    try:
        c = Control()
        #rospy.spin()
        while not (rospy.is_shutdown()):
            #Mode surveillance avec le drone qui tourne sur lui-meme
            mouvement = Twist()

            mouvement.linear.x = 0  
            mouvement.linear.y = 0
            mouvement.linear.z = 0
            mouvement.angular.x = 0
            mouvement.angular.y = 0 
            mouvement.angular.z = 0.5
            if (c.mode == 1):
                c.mouvement_pub.publish(mouvement)
            c.r.sleep()
    except rospy.ServiceException as exc:
        rospy.loginfo("control node terminated.")
        print("Service did not process request: " + str(exc))
