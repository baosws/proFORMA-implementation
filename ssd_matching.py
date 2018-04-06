import numpy as np
import stable_marriage as sm

INF = 10 ** 9
def SSD_non_normalized(img_src, img_dst):
    ssd = 0
    h, w = img_src.shape
    for i in range(h):
        for j in range(w):
            ssd += (img_src[i][j] - img_dst[i][j]) ** 2
    
    return ssd

def normalized(img):
    img = np.array(img, dtype=np.float64)
    h, w = img.shape
    mean = img.mean()
    img -= np.array([mean] * w)
    var = np.sum(img ** 2) ** 0.5
    img /= var
    return img
    
def SSD_normalized(img_src, img_dst):
    return SSD_non_normalized(normalized(img_src), normalized(img_dst))

def get_sub_img(pt, img_src, size):
    y, x = map(int, pt)
    h, w = img_src.shape
    if x - size + 1 >= 0 and x + size - 1 < h and y - size + 1 >= 0 and y + size - 1 < w:
        return np.array([[img_src[i][j] for j in range(y - size + 1, y + size)]
                                   for i in range(x - size + 1, x + size)])
    else:
        return None

def SSD_patch_img(keypoints, patch, img):
    return [SSD_normalized(patch, get_sub_img(point.pt, img, 3))
            for point in keypoints]

def distance(ptA, ptB):
    return ((ptA[0] - ptB[0]) ** 2 + (ptA[1] - ptB[1]) ** 2) ** 0.5

def SSD_img_img(kp_src, img_src, kp_dst, img_dst):
    n, m = len(kp_src), len(kp_dst)
    k = max(n, m)
    diameter = 3
    max_dist = 10
    patchtes_src = [get_sub_img(kp.pt, img_src, diameter) for kp in kp_src]
    patchtes_dst = [get_sub_img(kp.pt, img_dst, diameter) for kp in kp_dst]
    cost_mat = [[0] * k for i in range(k)]
    for i in range(k):
        for j in range(k):
            if i < n and j < m and distance(kp_src[i].pt, kp_dst[j].pt) < max_dist:
                cost_mat[i][j] = SSD_normalized(patchtes_src[i], patchtes_dst[j])
            else:
                cost_mat[i][j] = INF
            
    src_prefers = [[] for i in range(k)]
    dst_prefers = [[] for i in range(k)]
    for i in range(k):
        for j in range(k):
            src_prefers[i].append((cost_mat[i][j], j))
            dst_prefers[i].append((cost_mat[j][i], j))
        src_prefers[i].sort()
        dst_prefers[i].sort()
        for j in range(k):
            src_prefers[i][j] = src_prefers[i][j][1]
            dst_prefers[i][j] = dst_prefers[i][j][1]
    matchX, matchY = sm.marry(src_prefers, dst_prefers)
    return matchX, matchY, cost_mat
