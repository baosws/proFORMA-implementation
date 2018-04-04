import numpy as np
import cv2
from matplotlib import pyplot as plt
from ssd_matching import *
fig = plt.figure()

def camera_capture():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        fig.add_subplot(1, 2, 1)
        cv2.imshow('bgr', frame)
        fig.add_subplot(1, 2, 2)
        cv2.imshow('gray', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


def fast_matching():
    fast = cv2.FastFeatureDetector_create(type = cv2.FastFeatureDetector_TYPE_7_12, nonmaxSuppression = True)
    img_src = cv2.imread('./Pictures/Webcam/2018-04-03-104438.jpg', 0)
    img_dst = cv2.imread('./Pictures/Webcam/2018-04-03-104449.jpg', 0)
    kp_src = fast.detect(img_src, None)
    kp_dst = fast.detect(img_dst, None)

    img_src = cv2.drawKeypoints(img_src, kp_src, None)
    img_dst = cv2.drawKeypoints(img_dst, kp_dst, None)
#     img_dst = cv2.drawKeypoints(img_src, keypoints, None)
    
    fig.add_subplot(1, 2, 1)
    plt.imshow(img_src)
    fig.add_subplot(1, 2, 2)
    plt.imshow(img_dst)
 
#     ssd_img = SSD_keypoint(keypoints, get_sub_img(keypoints[10].pt, img_src, 3), img_src)
#     for point, ssd in zip(keypoints, ssd_img):
#         print(point.pt, ssd)

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

fast_matching()
plt.show()
# cv2.waitKey(0)
# cv2.destroyAllWindows()
