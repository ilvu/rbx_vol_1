#!/usr/bin/env python

"""
    Relax all servos by disabling the torque for each and set initial speed
    to a reasonable value.
"""
import roslib
roslib.load_manifest('rbx1_dynamixels')
import rospy, time
from dynamixel_controllers.srv import TorqueEnable, SetTorqueLimit, SetSpeed

class Relax():
    def __init__(self):
        rospy.init_node('relax_all_servos')
        
        dynamixels = rospy.get_param('dynamixels', '')
        
        default_dynamixel_speed = rospy.get_param('~default_dynamixel_speed', 0.5)
        default_dynamixel_torque = rospy.get_param('~default_dynamixel_torque', 0.5)

     
        speed_services = list()   
        torque_services = list()
        set_torque_limit_services = list()
            
        for name in sorted(dynamixels):
            controller = name.replace("_joint", "") + "_controller"
            
            torque_service = '/' + controller + '/torque_enable'
            rospy.wait_for_service(torque_service)  
            torque_services.append(rospy.ServiceProxy(torque_service, TorqueEnable))
            
            set_torque_limit_service = '/' + controller + '/set_torque_limit'
            rospy.wait_for_service(set_torque_limit_service)  
            set_torque_limit_services.append(rospy.ServiceProxy(set_torque_limit_service, SetTorqueLimit))
            
            speed_service = '/' + controller + '/set_speed'
            rospy.wait_for_service(speed_service)  
            speed_services.append(rospy.ServiceProxy(speed_service, SetSpeed))
        
        # Set the default speed to something small
        for set_speed in speed_services:
            try:
                set_speed(default_dynamixel_speed)
            except:
                pass
            
        # Set the torque limit to a moderate value
        for set_torque_limit in set_torque_limit_services:
            try:
                set_torque_limit(default_dynamixel_torque)
            except:
                pass

        # Relax all servos to give them a rest.
        for torque_enable in torque_services:
            try:
                torque_enable(False)
            except:
                pass
        
if __name__=='__main__':
    Relax()
