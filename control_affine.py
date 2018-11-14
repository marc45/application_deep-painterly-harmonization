import numpy as np
import cv2 
import manner_annote  as   manner

foreign="/Users/a11/Desktop/transfer_material/dsadasdasdsad.png"
foreign="/Users/a11/Desktop/transfer_material/569e220a21f29be933f37742.png"
target="/Users/a11/Desktop/transfer_material/img_4119.jpg"
target="/Users/a11/Desktop/transfer_material/5810_oqFTdt_FOMBQE8.jpeg"

fr_png = cv2.imread(foreign,-1)
target_img=cv2.imread(target)

def source_rect(img_png):
    #read png and find max rect 
    assert img_png.shape[2]==4
    mask = img_png[:,:,-1].copy()
    img = img_png[:,:,:3].copy()
    print img.shape,"===="

    ret,thresh = cv2.threshold(mask,127,255,0)

    _,contours,hierarchy = cv2.findContours(thresh, 1, 2)
    contours=sorted(contours,key=cv2.contourArea,reverse=True)
    cnt = contours[0]

    cnt = np.int0(cnt)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img,[box],0,(0,0,255),2)
    cv2.drawContours(mask,[box],0,255,-1)
    return img,mask,box


def draw_img_withpoints(img,box):
    cv2.drawContours(img,[box],0,(0,0,255),2)
    return img

#while(True):
cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
#cv2.namedWindow("Camera",cv2.WINDOW_NORMAL)
if True:
    im_src,mask_src ,box_src = source_rect(fr_png)
    box_src = manner.get_rect_four_points(box_src.tolist())

    pt4_dst = manner.get_four_points(target_img)
    box_dst = manner.get_rect_four_points(pt4_dst.tolist())

#    img_cpy = manner.draw_four_points(img,pt.tolist())
#    cv2.imshow("a",img_cpy)
#    cv2.waitKey(0)

    frame = manner.affine_poly(im_src,box_src,target_img,box_dst)

    # display the camera and masked images
    cv2.imshow('Image', frame)
    cv2.waitKey(0)
    #if cv2.waitKey(5) & 0xFF == ord('q'):
    #    break

# clean up our resources
cv2.destroyAllWindows()
