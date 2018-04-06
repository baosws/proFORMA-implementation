import numpy as np
import cv2
from matplotlib import pyplot as plt
import ssd_matching
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

def normalized(img):
    img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    kernel_size = 2
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
    img = cv2.filter2D(img, -1, kernel)
    return img

def fast_matching():
    fast = cv2.FastFeatureDetector_create(type = cv2.FastFeatureDetector_TYPE_7_12, nonmaxSuppression = True)
    img_src = cv2.imread('./P_20180406_171031.jpg', 0)
    img_dst = cv2.imread('./P_20180406_171029.jpg', 0)

    # half-sampling
    img_src = normalized(img_src)
    img_dst = normalized(img_dst)
    
    # get keypoints
    kp_src = fast.detect(img_src, None)
    kp_dst = fast.detect(img_dst, None)

    # matching
    matchX, matchY, cost_mat = ssd_matching.SSD_img_img(kp_src, img_src, kp_dst, img_dst)
    dmatch = [cv2.DMatch(i, matchX[i], cost_mat[i][matchX[i]]) for i in range(len(kp_src)) if matchX[i] < len(kp_dst)]
    dmatch.sort(key = lambda x: x.distance)

    # draw matches
    img_res = cv2.drawMatches(img_src, kp_src, img_dst, kp_dst, dmatch[:50], outImg = None, flags = 2)
#     img_dst = cv2.drawKeypoints(img_src, keypoints, None)
#     
#     fig.add_subplot(1, 2, 1)
#     plt.imshow(img_src)
#     fig.add_subplot(1, 2, 2)
#     plt.imshow(img_dst)
    plt.imshow(img_res)
#     ssd_img = SSD_keypoint(keypoints, get_sub_img(keypoints[10].pt, img_src, 3), img_src)
#     for point, ssd in zip(keypoints, ssd_img):
#         print(point.pt, ssd)

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

fast_matching()
plt.show()
# cv2.waitKey(0)
# cv2.destroyAllWindows()
