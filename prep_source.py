import cv2
import numpy as np 
import os 




p1="/Users/a11/Desktop/transfer_material/image-43.png"
p1_m="/Users/a11/Desktop/transfer_material/mask-image-43.png"
p1_m="/Users/a11/Desktop/transfer_material/image-43.png-matting.jpg"

p1_t_info=("/Users/a11/Desktop/transfer_material/pisa014.jpg",0.9)
#p1_t_info=("/Users/a11/Desktop/transfer_material/Leaning-Tower-of-Pisa-compressor.jpg",0.3)
#p1_t_info=("/Users/a11/Desktop/transfer_material/leaning-tower-of-pisa-1427012597XXV.jpg",0.6)

#p1_t_info=("/Users/a11/Desktop/transfer_material/69e002b103bc46da85825205838e1f71.jpg" ,0.7) 



p1_img=cv2.imread(p1)
p1_m_img=cv2.imread(p1_m,-1)
p1_t,entiy_ratio=p1_t_info
p1_t_img=cv2.imread(p1_t)

print p1_m_img.shape
assert  len(p1_m_img.shape)==2 or  p1_m_img.shape[2]==4  , "not mask"
if len(p1_m_img.shape)>2:
    p1_m_img=cv2.cvtColor(p1_m_img,cv2.COLOR_BGR2GRAY)
def resize_padding(rgb,mask,expect_size,entiy_ratio=0.2,padding="left"):
    assert padding in ["left","right","center"]
    assert entiy_ratio <=1 
    w,h=expect_size[:2]
    w1,h1=rgb.shape[:2]
    if h1>w1 :
        ratio = w1/float(h1)
        new_w = w 
        new_h = new_w* ratio 
    
    else :
        ratio = h1/float(w1)
        new_h = h 
        new_w = new_h* ratio 
    new_w,new_h=int(new_w),int(new_h)

    blank=np.zeros(expect_size,dtype=np.uint8)
    new_rgb=cv2.resize(rgb,(new_w,new_h))
    new_rgb=cv2.resize(new_rgb,None,fx=entiy_ratio,fy=entiy_ratio)
    blank[-new_rgb.shape[0]:,:new_rgb.shape[1],:]=new_rgb
    

    blank_mask=np.zeros(expect_size[:2],dtype=np.uint8)
    new_mask=cv2.resize(mask,(new_w,new_h),interpolation=cv2.INTER_NEAREST)
    print "b...",new_mask.shape
    new_mask=cv2.resize(new_mask,None,fx=entiy_ratio,fy=entiy_ratio)
    print "a/...",new_mask.shape,ratio
    blank_mask[-new_mask.shape[0]:,:new_mask.shape[1]]=new_mask
    return blank,blank_mask

if p1_t_img.shape!=p1_img.shape:
    #p1_img=cv2.resize(p1_img,p1_t_img.shape[:2][::-1],)
    #p1_m_img=cv2.resize(p1_m_img,p1_t_img.shape[:2][::-1],interpolation=cv2.INTER_NEAREST)
    p1_img,p1_m_img = resize_padding(p1_img,p1_m_img, p1_t_img.shape,entiy_ratio=entiy_ratio)

p1_m_img[p1_m_img>0]=1
p1_m_img=p1_m_img.astype(np.float32)


alpha=p1_m_img.copy()
if len(alpha.shape)<=2 :
    alpha=cv2.merge([alpha,alpha,alpha])
foreground_e=p1_img.copy().astype(np.float32)
background_e=p1_t_img.copy().astype(np.float32)

print alpha.shape,alpha.dtype,foreground_e.shape,foreground_e.dtype

foreground = cv2.multiply(alpha, foreground_e)
background = cv2.multiply((1.0 - alpha)*1.0, background_e)

outImage = cv2.add(foreground, background)

print np.unique(outImage)

outImage = outImage.astype(np.uint8)
cv2.namedWindow("a",cv2.WINDOW_NORMAL)
cv2.imshow("a",outImage)
cv2.waitKey(0)




print p1_m_img.shape,p1_img.shape,p1_t_img.shape


