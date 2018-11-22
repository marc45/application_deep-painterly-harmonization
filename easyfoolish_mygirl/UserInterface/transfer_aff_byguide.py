'''
Created on Nov 21, 2018

@author: wangjian7
'''
from __future__ import print_function,absolute_import,unicode_literals

import cv2
import numpy as np 

import util

def crop_minAreaRect(img, rect):

    # rotate img
    angle = rect[2]
    rows,cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]    
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1], 
                       pts[1][0]:pts[2][0]]

    return img_crop

def draw_mmm(surce_img,source_mask,target_img):
    def source_rect(img,mask):
        img = cv2.bitwise_and(img,img,mask=mask)
        #read png and find max rect 
        _,contours,hierarchy = cv2.findContours(mask, 1, 2)
        contours=sorted(contours,key=cv2.contourArea,reverse=True)
        cnt = contours[0]
      
        cnt = np.int0(cnt)
        rect = cv2.minAreaRect(cnt)

        b,g,r=cv2.split(img)
        img_png = cv2.merge([b,g,r,mask])
        
        cropped_img_png = crop_minAreaRect(img_png,rect)
        b,g,r,cropped_mask=cv2.split(cropped_img_png)
        cropped_img=cv2.merge([b,g,r])

        h,w = cropped_img.shape [:2]
        box=util.get_rect_four_points([[w,h],[0,h],[0,0],[w,0]])
        return cropped_img,cropped_mask*255,box
 
    im_src,mask_src ,_ = source_rect(surce_img,source_mask)
    h,w = mask_src.shape
    box_src=[ [0,0],[h,0],[w,h],[0,w]]
#     
    ##prompt user clockwise annote four points 
    pt4_dst = util.get_four_points(target_img)
    pt4_dst = map(list,pt4_dst)
    #items=[]
    box_dst = np.array(list(pt4_dst)).astype(np.int64)
    box_dst = box_dst .tolist()
    box_dst=np.array(box_dst)
    box_src=np.array(box_src)
    


    frame,alpha = util.affine_poly(im_src,mask_src,box_src,target_img,box_dst)
 
    cv2.imshow('Image', frame)
    cv2.waitKey(0)
#     cv2.imshow('Image', (alpha*255).astype(np.uint8) )
    cv2.imwrite("0_naive.jpg",frame)
    cv2.imwrite("0_c_mask.jpg",alpha*255)
    cv2.imwrite("0_c_mask_dilated.jpg",alpha*255)
    cv2.imwrite("0_target.jpg",target_img)
    
    print ("save success")



if __name__=="__main__":
#     import unittest 
# #     cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
#     import sys,os
#     class xx (unittest.TestCase):
#         def setUp(self):
#             p1= "t1_img.jpg"
#             p1_m= "t1_img_mask.png"
#             self.img = cv2.imread(p1,-1)
#             self.img_mask = cv2.imread(p1_m,-1)
#             p2 = "./images/83dff40e87d730719bcc8be9fdda2726.jpg"
#             self.target_img =cv2.imread(p2)
#             assert len(self.img_mask.shape)==2 
#             assert len(self.img.shape)==3 
#             
#         def test_x1(self):
#             import sys ,os 
#             p=sys.argv[1]
#             if not os.path.isfile(p) :
#                 raise Exception("not exist")
#             p2 = p
#             self.target_img =cv2.imread(p2)
# #             img_crop =cv2.bitwise_and(self.img,self.img ,mask =self.img_mask)
#             
#             draw_mmm(self.img,self.img_mask,self.target_img) 
#         
#     
#     unittest.main()

    import sys,os
    class obj :
        def test_x1(self):
            p1= "t1_img.jpg"
            p1_m= "t1_img_mask.png"
            self.img = cv2.imread(p1,-1)
            self.img_mask = cv2.imread(p1_m,-1)
            p2 = "./images/83dff40e87d730719bcc8be9fdda2726.jpg"
            self.target_img =cv2.imread(p2)
            assert len(self.img_mask.shape)==2 
            assert len(self.img.shape)==3 
            
            import sys ,os 
            p=sys.argv[1]
            if not os.path.isfile(p) :
                raise Exception("not exist")
            p2 = p
            self.target_img =cv2.imread(p2)
#             img_crop =cv2.bitwise_and(self.img,self.img ,mask =self.img_mask)
            
            draw_mmm(self.img,self.img_mask,self.target_img) 
        
    
    obj().test_x1()
    