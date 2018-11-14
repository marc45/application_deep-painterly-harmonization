import cv2
import  numpy as np  


fp=np.array( [[299. ,331.],
 [319., 410.],
 [458., 468.],
 [582., 451.]] )


img=np.zeros((600,600,3),dtype=np.uint8)


fp = np.expand_dims(fp,axis=1)

cnt= fp
cnt = np.int0(cnt)

rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img,[box],0,(0,0,255),2)



cv2.imshow("img",img)
cv2.waitKey(0)

