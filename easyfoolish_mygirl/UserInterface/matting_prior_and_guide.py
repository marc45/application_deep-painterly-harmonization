'''
Created on Nov 15, 2018

@author: wangjian7
'''
from __future__ import print_function,absolute_import,unicode_literals

import cv2
import numpy as np 
from easyfoolish_mygirl.common import mq_dataset
from easyfoolish_mygirl.common import Jconfig
import util 



def mouse_handler(event, x, y, flags, data) :

    if event == cv2.EVENT_LBUTTONDOWN :
#         img = data["im"]

        mask_list = data["mask"]
        index=np.max(mask_list[:,y,x])
#         print (index,"----")
        if index == 0 :
            return  
        mask = mask_list[index]
#         print (np.unique(mask))
        _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        img = data['im'].copy()
#         print ("find ..","/",len(contours))
        for i,cnt in enumerate(contours ):
            dist3 = cv2.pointPolygonTest(cnt, (x,y), True)
            if dist3 >=0:
                
                if len(cnt) <=4 :
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(img,[box],0,(255,255,255),2)
                else:
                    ellipse = cv2.fitEllipse(cnt)
                    cv2.ellipse(img,ellipse,(255,255,255),2)
            
                data['index'].append(index)
        cv2.circle(img, (x,y),10, (0,0,255), -1, 16);

        cv2.imshow("Image", img);
        
        data['points'].append([x,y])

def choice_mask_floors(im,mask):

    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['mask'] = mask.copy()
    data['index'] = []
    data['points'] = []

    #Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)

    # Convert array to np.array
#     points = np.vstack(data['points']).astype(float)
    if len(data['index'] )<=0 :
        raise Exception("pls choice one ")
    print (data['index']  )
    index = int(data['index'][-1])
    index = index if 0<index< mask.shape[0] else 0
    return im,mask[index].copy()


# def manual_prior_guide(img,mask_hirency):
#     '''
#     A user interface GUI to annote a rect or polygon with user's favourite proposal area
#     '''
#     w,h=img.shape[:2]
#     mask = np.zeros((w,h),dtype=np.uint8)
# 
#     all_pts = util.get_four_points(img)
#     if len(all_pts)==4:
#         '''
#         rectage guess
#         '''
#         box = util.get_rect_four_points(all_pts.tolist())
#     else:
#         cnt=np.expand_dims( np.array(all_pts) ,axis=1)
#         cnt = np.int0(cnt)
#         epsilon = 0.1*cv2.arcLength(cnt,True)
#         approx = cv2.approxPolyDP(cnt,epsilon,True)
#         box = approx
# 
#     cv2.drawContours(img,[box],0,(0,0,255),2)
#     cv2.drawContours(mask,[box],0,255,-1)
#     return img,mask

def util_cover_mask(img,mask_list ):
    '''
    mask cover in img with alpha*A+(1-alpha)*B
    param :
    mask_list [mask1,mask2,mask3,...]
        mask1.shape == w,h 
        unique(mask1),unique(mask2),unique(mask3),...=1,2,3...
    '''
    mask=np.zeros(img.shape[:2],dtype=np.uint8)
    for m in mask_list:
        if np.sum(m)==0:
            continue
        mask=cv2.bitwise_or(mask,m)
        mask[mask!=0]=255
    mask_rgb=cv2.merge([mask]*3)
    dst = cv2.addWeighted(img,0.3,mask_rgb,0.7,0)
    return dst 




if __name__=="__main__":
    cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
    #mock data 
#     4 rect  :two of them was nest each other
#     import unittest 
#     class x (unittest.TestCase):
#         def test_mock_inter_rectanges(self):
#             blank=np.zeros((500,500,3),dtype=np.uint8)
#             mask=np.zeros((500,500),dtype=np.uint8)
#             #1 
#             mask_1=mask.copy()
#             p1_box=[[50,50],[50,0],[0,0],[0,50],]
#             p1_box=np.expand_dims(np.array(p1_box),axis=1)
#             cv2.drawContours(blank,[p1_box],0,(0,0,255),-1)
#             cv2.drawContours(mask_1,[p1_box],0,1,-1)
#             
#             #2
#             mask_2=mask.copy()
#             
#             p1_box=[[500,500],[500,450],[450,450],[450,500],]
#             p1_box=np.expand_dims(np.array(p1_box),axis=1)
#             cv2.drawContours(blank,[p1_box],0,(0,0,255),-1)
#             cv2.drawContours(mask_2,[p1_box],0,2,-1)
#             
#             #3
#             mask_3=mask.copy()
#             
#             cv2.rectangle(blank,tuple([200,200]),tuple([300,300]),(0,0,255),-1)
#             cv2.rectangle(mask_3,tuple([200,200]),tuple([300,300]),3,-1)
#             
#             #4 
#             mask_4=mask.copy()
#             
#             cv2.rectangle(blank,tuple([150,250]),tuple([250,350]),(0,255,255),-1)
#             cv2.rectangle(mask_4,tuple([150,250]),tuple([250,350]),4,-1)
#             
#             #4.1 
#             cv2.rectangle(blank,tuple([275,150]),tuple([350,250]),(0,255,255),-1)
#             cv2.rectangle(mask_4,tuple([275,150]),tuple([350,250]),4,-1)
#             
#             all_mask=np.array([mask_1,mask_2,mask_3,mask_4])
#             choice_mask_floors(blank,all_mask)
#             cv2.imshow("a",blank)
#             cv2.waitKey(0)
# 
#         def test_input_(self):
#                     
#             rgb=cv2.imread("./images/2009_000223.jpg")
#             mask=cv2.imread("./images/2009_000223.png",-1)
#             all_mask=[]
#             for i,c in enumerate(np.unique(mask)):
#                 if c==0 :
#                     continue
#                 blk=np.zeros(mask.shape,dtype=np.uint8)
#                 blk[mask==c]=i
#                 all_mask.append(blk)
#             all_mask=np.array(all_mask)
#             
#             choice_mask_floors(rgb,all_mask)
#         #     cv2.imshow("a",b)
#         #     cv2.waitKey(0)
    
#         def test_mq(self):
#             image=cv2.imread("./images/2009_000223.jpg")
#             print ("send...")
#             msg_id_list = mq_dataset.intermediate_job_finish("detectron", [image])
#             
#             msg_id = msg_id_list[0]
#             furture_id , _= mq_dataset.build_key(msg_id,"detectron_result")
#             
#             
#             print (furture_id,"222")
#             while True :
#                 if mq_dataset.is_exist(furture_id):
#                     get_data=mq_dataset.get_msg_info(furture_id)
#                 
#                     _,matting_list = get_data
#                     for i,matting_rd in enumerate(matting_list):
#                         print ((matting_rd.shape),".....")
#                         matting=np.array(matting_rd.copy())
#                         matting[matting>0]=255
#                         
#                         cv2.imwrite("a_%d.jpg"%(i),matting)
#                         print (type(matting),matting.shape ,np.unique(matting,return_counts=True))
#                     break
    if True :    
        def test_mmq(self):
            import sys ,os 
            p=sys.argv[1]
            if not os.path.isfile(p) :
                raise Exception("not exist")
            
            print ("will read",p)
#             image=cv2.imread("./images/295b37832c0db6470a855640d6510c04.jpg")
            image=cv2.imread(p)
#             target_image=cv2.imread("./images/19064748793_bb942deea1_k.jpg")
            print ("send...")
            msg_id_list = mq_dataset.intermediate_job_finish("detectron", [image])
             
            msg_id = msg_id_list[0]
            furture_id , _= mq_dataset.build_key(msg_id,"detectron_result")
             
             
            print (furture_id,"222")
            while True :
                if mq_dataset.is_exist(furture_id):
                    get_data=mq_dataset.get_msg_info(furture_id)
                    _,matting_list = get_data
                    
                    bl=[np.zeros(matting_list.shape[1:],dtype=np.uint8)]
                    for i,m in enumerate(matting_list):
                        m=(m//255)*(i+1)
                        bl.append(m)
                        mm=m.copy()
                        mm[m!=0]=255
                    print (len(bl),len(matting_list))
                    print (np.unique(np.array(bl)))
                    ###cover mask
                    source_img = image.copy()
                    new_img = util_cover_mask(image,bl) 
                    img,mask = choice_mask_floors(new_img,np.array(bl) )
                    
                    cv2.imwrite("t1_img.jpg",image)
                    cv2.imwrite("t1_img_mask.png",mask)
                    print ("save success")
                    break

    test_mmq(None)
#     unittest.main()
