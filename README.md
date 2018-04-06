# proFORMA-implementation

## Introduction
An attempt to implement an online 3d-reconstruction algorithm from this paper:
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.480.8901&rep=rep1&type=pdf

## In progress: Robust Point Tracker
Tracking on 2 images:
- Pre-processing: each image is half-sampled (resize by 0.5 on each dimension) and blurred before processing.
- Extracted keypoints from each image using FAST feature with non-maximal suppression (https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_fast/py_fast.html).
- Two set of keypoints are matched using stable marriage algorithm (https://en.wikipedia.org/wiki/Stable_marriage_problem), using SSD (http://www.cse.psu.edu/~rtc12/CSE486/lecture07.pdf) as cost function between two keypoints.

Some results:

![](/results/Screenshot from 2018-04-06 17-15-11.png)
