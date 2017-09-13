#! /usr/bin/env python
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import sys
import numpy as np
from std_msgs.msg import String



class img_converter:


	def __init__(self):
		self.bridge=CvBridge()
		self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.ros_cv_converter)
 	
 	def ros_cv_converter(self,data):
  
	   	try:
	   		cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError,e:
			print("==[CAMERA MANAGER]==", e)

		#(rows,cols,channels) = cv_image.shape
		#if cols > 60 and rows > 60 :
		#	cv2.circle(cv_image, (50,50), 10, 255)

		hsv=cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)


		lower_blue= np.array([110,50,50])
		upper_blue= np.array([130,255,255])

		mask =cv2.inRange(hsv,lower_blue,upper_blue)
		res= cv2.bitwise_and(cv_image,cv_image,mask=mask)

		cv2.imshow("frame",cv_image)
		cv2.imshow("mask",mask)
		cv2.imshow("res",res)
		cv2.waitKey(3)

		#try: 
		#	self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		#except CvBridgeError as e:
		#	print(e)


def main(args):
	rospy.init_node('image_converter', anonymous=True)
	ic= img_converter()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()



if __name__ == '__main__':
	main(sys.argv)
