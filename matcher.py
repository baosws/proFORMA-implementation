import ssd_matching as sm
import stable_marriage_matching as smm
import hungarian_matching as hm
INF = 10 ** 9

def distance(ptA, ptB):
    return ((ptA[0] - ptB[0]) ** 2 + (ptA[1] - ptB[1]) ** 2) ** 0.5

def stable_SSD(img_src, kp_src, img_dst, kp_dst, diameter = 3, max_dist = INF):
    n, m = len(kp_src), len(kp_dst)
    k = max(n, m)
    patchtes_src = [sm.get_sub_img(kp.pt, img_src, diameter) for kp in kp_src]
    patchtes_dst = [sm.get_sub_img(kp.pt, img_dst, diameter) for kp in kp_dst]
    cost_mat = [[0] * k for i in range(k)]
    for i in range(k):
        for j in range(k):
            if i < n and j < m and distance(kp_src[i].pt, kp_dst[j].pt) < max_dist:
                cost_mat[i][j] = sm.SSD_normalized(patchtes_src[i], patchtes_dst[j])
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
    matchX, matchY = smm.marry(src_prefers, dst_prefers)
    return matchX, matchY, cost_mat

def hungarian_SSD(img_src, kp_src, img_dst, kp_dst, diameter = 3, max_dist = INF):
    n, m = len(kp_src), len(kp_dst)
    k = max(n, m)
    patchtes_src = [sm.get_sub_img(kp.pt, img_src, diameter) for kp in kp_src]
    patchtes_dst = [sm.get_sub_img(kp.pt, img_dst, diameter) for kp in kp_dst]
    cost_mat = [[0] * k for i in range(k)]
    for i in range(k):
        for j in range(k):
            if i < n and j < m and distance(kp_src[i].pt, kp_dst[j].pt) < max_dist:
                cost_mat[i][j] = sm.SSD_normalized(patchtes_src[i], patchtes_dst[j])
            else:
                cost_mat[i][j] = INF
    matchX, matchY = hm.hungarian_match(cost_mat)
    return matchX, matchY, cost_mat
