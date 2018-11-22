from __future__ import print_function,absolute_import,unicode_literals

import cv2
import numpy as np 

import util

'''
A user interface GUI to annote a rect or polygon on favourite proposal's area
'''
def manual_annoting(img):
    w,h=img.shape[:2]
    mask = np.zeros((w,h),dtype=np.uint8)

    all_pts = util.get_four_points(img)
    if len(all_pts)==4:
        '''
        rect guess
        '''
        box = util.get_rect_four_points(all_pts.tolist())
    else:
        cnt=np.expand_dims( np.array(all_pts) ,axis=1)
        cnt = np.int0(cnt)
        epsilon = 0.1*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        box = approx

    cv2.drawContours(img,[box],0,(0,0,255),2)
    cv2.drawContours(mask,[box],0,255,-1)
    return img,mask



if __name__=="__main__":
    cv2.namedWindow("a",cv2.WINDOW_NORMAL)

    p="/Users/a11/Desktop/transfer_material/569e220a21f29be933f37742.jpg"
    img=cv2.imread(p)

    rgb,mask=manual_annoting(img)
    cv2.imshow("a",mask)
    cv2.waitKey(0)




