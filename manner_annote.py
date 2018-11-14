import cv2
import numpy as np
'''
https://www.learnopencv.com/homography-examples-using-opencv-python-c/
'''

def mouse_handler(event, x, y, flags, data) :
    
    if event == cv2.EVENT_LBUTTONDOWN :
        w,h,_=data['im'].shape
        circle_radiu=3*int(np.log2(w))

        cv2.circle(data['im'], (x,y),circle_radiu, (0,0,255), -1, 16);
        cv2.circle(data['im'], (x,y),int(circle_radiu*1.2), (255,255,0), 2, 16);
        cv2.imshow("Image", data['im']);
        if len(data['points']) < 4 :
            data['points'].append([x,y])

def get_four_points(im):
    
    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['points'] = []
    
    #Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)
    
    # Convert array to np.array
    points = np.vstack(data['points']).astype(float)
    
    return points

def get_rect_four_points(points=[]):
    assert type(points) == list 

    cnt=np.array(points)
    if len(cnt.shape)==2 :
        cnt=np.expand_dims(cnt,axis=1)

    assert cnt.shape[2]==2

    cnt = np.int0(cnt)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    #cv2.drawContours(img,[box],0,(0,0,255),2)
    #return img
    return box


def affine_poly(im_src ,src_box ,im_dst ,dst_box):
    assert np.array(src_box).shape==(4,2),"""
    expect box is [[12 12]
     [ 0 12]
     [ 0  0]
     [12  0]]
     """
    pts_src = np.array(src_box).astype(np.float32)
    pts_dst = np.array(dst_box).astype(np.float32)

    # Calculate Homography between source and destination points
    h, status = cv2.findHomography(pts_src, pts_dst);
    
    # Warp source image
    im_temp = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
    # Black out polygonal area in destination image.
    cv2.fillConvexPoly(im_dst, pts_dst.astype(int), 0, 16);
    # Add warped source image to destination image.
    im_dst = im_dst + im_temp;

    return im_dst



if __name__=="__main__":
    p="/Users/a11/Desktop/transfer_material/0005018340019789_b.jpg"
    img=cv2.imread(p)
    pt = get_four_points(img)
    print pt.shape

    img_cpy=draw_four_points(img,pt.tolist())
    cv2.imshow("a",img_cpy)
    cv2.waitKey(0)

