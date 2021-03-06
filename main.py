import numpy as np
import cv2
from matplotlib import pyplot as plt
import matcher
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
    # half-sampling
    img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    # filter
    kernel_size = 2
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
    img = cv2.filter2D(img, -1, kernel)
    return img

def fast_matching():
    fast = cv2.FastFeatureDetector_create(type = cv2.FastFeatureDetector_TYPE_7_12, nonmaxSuppression = True)
    img_src = cv2.imread('./resource/P_20180407_120033.jpg', 0);
    img_dst = cv2.imread('./resource/P_20180407_120034.jpg', 0);

    # normalize
    img_src = normalized(img_src)
    img_dst = normalized(img_dst)
    
    # get keypoints
    kp_src = fast.detect(img_src, None)
    kp_dst = fast.detect(img_dst, None)

    # matching
    matchX, matchY, cost_mat = matcher.stable_SSD(img_src, kp_src, img_dst, kp_dst, max_dist = 25)
    dmatch = [cv2.DMatch(i, matchX[i], cost_mat[i][matchX[i]]) for i in range(len(kp_src)) if matchX[i] < len(kp_dst)]
    dmatch.sort(key = lambda x: x.distance)
    
    # draw matches
    img_res = cv2.drawMatches(img_src, kp_src, img_dst, kp_dst, dmatch[:int(0.2 * len(dmatch))], outImg = None, flags = 2)
     
#     fig.add_subplot(1, 2, 1)
#     plt.imshow(img_src)
#     fig.add_subplot(1, 2, 2)
#     plt.imshow(img_dst)
    plt.imshow(img_res)

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

fast_matching()
plt.show()
# cv2.waitKey(0)
# cv2.destroyAllWindows()
