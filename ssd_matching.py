import numpy as np

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

def SSD_img_img(kp_src, img_src, kp_dst, img_dst):
    n = len(kp_src)
    m = len(kp_dst)
    src_prefers = [[0] * m for i in range(n)]
    dst_prefers = [[0] * n for i in range(h)]
    fo
    
