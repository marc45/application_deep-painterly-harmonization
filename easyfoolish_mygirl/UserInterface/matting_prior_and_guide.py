'''
Created on Nov 15, 2018

@author: wangjian7
'''

import cv2
import numpy as np 

def mouse_handler(event, x, y, flags, data) :

    if event == cv2.EVENT_LBUTTONDOWN :
#         img = data["im"]

        mask_list = data["mask"]
        index=np.max(mask_list[:,y,x])
        if index == 0 :
            return  
        mask = mask_list[index-1]
        
        _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for i,cnt in enumerate(contours ):
            dist3 = cv2.pointPolygonTest(cnt, (x,y), True)
            if dist3 >=0:
                print "find ..",i,"/",len(contours)
                if len(cnt) <=4 :
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(data['im'],[box],0,(255,255,255),2)
                else:
                    ellipse = cv2.fitEllipse(cnt)
                    cv2.ellipse(data['im'],ellipse,(255,255,255),2)
            
        cv2.circle(data['im'], (x,y),10, (0,0,255), -1, 16);

        cv2.imshow("Image", data['im']);
        
        data['points'].append([x,y])

def choice_mask_floors(im,mask):

    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['mask'] = mask.copy()
    data['points'] = []

    #Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)

    # Convert array to np.array
    points = np.vstack(data['points']).astype(float)

    return points


'''
A user interface GUI to annote a rect or polygon with user's favourite proposal area
'''
def manual_prior_guide(img,mask_hirency):
    w,h=img.shape[:2]
    mask = np.zeros((w,h),dtype=np.uint8)

    all_pts = util.get_four_points(img)
    if len(all_pts)==4:
        '''
        rectage guess
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
    ##mock data 
    #4 rect  :two of them was nest each other
#     blank=np.zeros((500,500,3),dtype=np.uint8)
#     mask=np.zeros((500,500),dtype=np.uint8)
#     #1 
#     mask_1=mask.copy()
#     p1_box=[[50,50],[50,0],[0,0],[0,50],]
#     p1_box=np.expand_dims(np.array(p1_box),axis=1)
#     cv2.drawContours(blank,[p1_box],0,(0,0,255),-1)
#     cv2.drawContours(mask_1,[p1_box],0,1,-1)
#     
#     #2
#     mask_2=mask.copy()
# 
#     p1_box=[[500,500],[500,450],[450,450],[450,500],]
#     p1_box=np.expand_dims(np.array(p1_box),axis=1)
#     cv2.drawContours(blank,[p1_box],0,(0,0,255),-1)
#     cv2.drawContours(mask_2,[p1_box],0,2,-1)
#     
#     #3
#     mask_3=mask.copy()
# 
#     cv2.rectangle(blank,tuple([200,200]),tuple([300,300]),(0,0,255),-1)
#     cv2.rectangle(mask_3,tuple([200,200]),tuple([300,300]),3,-1)
# 
#     #4 
#     mask_4=mask.copy()
# 
#     cv2.rectangle(blank,tuple([150,250]),tuple([250,350]),(0,255,255),-1)
#     cv2.rectangle(mask_4,tuple([150,250]),tuple([250,350]),4,-1)
# 
#     #4.1 
#     cv2.rectangle(blank,tuple([275,150]),tuple([350,250]),(0,255,255),-1)
#     cv2.rectangle(mask_4,tuple([275,150]),tuple([350,250]),4,-1)
# 
#     all_mask=np.array([mask_1,mask_2,mask_3,mask_4])
#     choice_mask_floors(blank,all_mask)
#     cv2.imshow("a",blank)
#     cv2.waitKey(0)


    rgb=cv2.imread("./images/2009_000223.jpg")
    mask=cv2.imread("./images/2009_000223.png",-1)
    all_mask=[]
    for i,c in enumerate(np.unique(mask)):
        if c==0 :
            continue
        blk=np.zeros(mask.shape,dtype=np.uint8)
        blk[mask==c]=i
        all_mask.append(blk)
    all_mask=np.array(all_mask)
    
    choice_mask_floors(rgb,all_mask)
#     cv2.imshow("a",b)
#     cv2.waitKey(0)
    



