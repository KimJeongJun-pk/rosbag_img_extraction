import os
import rosbag
import cv2
import numpy as np
from cv_bridge import CvBridge
import rospy

output_folder = '/home/kimjeongjun/calibration_data/08.26/camera_calibration/'
camera_folder = os.path.join(output_folder, 'camera_images')

if not os.path.exists(camera_folder):
    os.makedirs(camera_folder)

bag_file = '/home/kimjeongjun/rosbag/08.26/camera_rosbag1.bag'

bridge = CvBridge()

camera_topic = '/camera/color/image_raw'

camera_images = []
camera_timestamps = []

bag = rosbag.Bag(bag_file)

for topic, msg, t in bag.read_messages(topics=[camera_topic]):
    if topic == camera_topic:
        try:
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            camera_images.append(cv_image)
            camera_timestamps.append(t.to_sec())
        except Exception as e:
            print(f"Image conversion failed: {e}")

bag.close()

for idx, img in enumerate(camera_images):
    image_filename = os.path.join(camera_folder, f'image_{idx:04d}.png')
    cv2.imwrite(image_filename, img)

print(f"카메라 이미지가 {camera_folder}에 저장되었습니다.")
