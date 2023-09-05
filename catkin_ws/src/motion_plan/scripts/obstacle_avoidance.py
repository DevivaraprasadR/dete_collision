#! /usr/bin/env python3

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None

def callback_laser(msg):
  # 120 degrees into 3 regions
  regions = {
    'right':  min(min(msg.ranges[0:2]), 10),
    'front':  min(min(msg.ranges[3:5]), 10),
    'left':   min(min(msg.ranges[6:9]), 10),
  }
  
  take_action(regions)
  
def take_action(regions):
  threshold_dist = 1.5
  linear_speed = 0.6
  angular_speed = 1

  msg = Twist()
  linear_x = 0
  angular_z = 0
  
  state_description = ''
  
  if regions['front'] > threshold_dist and regions['left'] > threshold_dist and regions['right'] > threshold_dist:
    state_description = 'No Obstacle Around'
    linear_x = linear_speed
    angular_z = 0
  elif regions['front'] < threshold_dist and regions['left'] < threshold_dist and regions['right'] < threshold_dist:
    state_description = 'Obstacle at: Front and Left and Right'
    linear_x = -linear_speed
    angular_z = angular_speed # Increase this angular speed for avoiding obstacle faster
  elif regions['front'] < threshold_dist and regions['left'] > threshold_dist and regions['right'] > threshold_dist:
    state_description = 'Obstacle at: Front'
    linear_x = 0
    angular_z = angular_speed
  elif regions['front'] > threshold_dist and regions['left'] > threshold_dist and regions['right'] < threshold_dist:
    state_description = 'Obstacle at: Right'
    linear_x = 0
    angular_z = -angular_speed
  elif regions['front'] > threshold_dist and regions['left'] < threshold_dist and regions['right'] > threshold_dist:
    state_description = 'Obstacle at: Left'
    linear_x = 0
    angular_z = angular_speed
  elif regions['front'] < threshold_dist and regions['left'] > threshold_dist and regions['right'] < threshold_dist:
    state_description = 'Obstacle at: Front and Right'
    linear_x = 0
    angular_z = -angular_speed
  elif regions['front'] < threshold_dist and regions['left'] < threshold_dist and regions['right'] > threshold_dist:
    state_description = 'Obstacle at: Front and Left'
    linear_x = 0
    angular_z = angular_speed
  elif regions['front'] > threshold_dist and regions['left'] < threshold_dist and regions['right'] < threshold_dist:
    state_description = 'Obstacle at: Left and Right'
    linear_x = linear_speed
    angular_z = 0
  else:
    state_description = 'Unknown Case'
    rospy.loginfo(regions)

  rospy.loginfo(state_description)
  msg.linear.x = linear_x
  msg.angular.z = angular_z
  pub.publish(msg)

def main():
  global pub
  
  rospy.init_node('reading_laser')
  
  pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
  
  sub = rospy.Subscriber('/robot/laser/scan', LaserScan, callback_laser)
  
  rospy.spin()

if __name__ == '__main__':
  main()

