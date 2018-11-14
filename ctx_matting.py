import os
import cv2
import numpy as np 



def method_manual(img):
    pass
    
    #return binary_mask 


def method_mutli_instance_choice(img):
    '''
    automatically  detected by  MaskRcnn 
    promote user-interface to annote user interesting box
    '''
    pass 

def method_interesting_people(img):
    '''
    xiaomi inner pre_trained 

    '''
    pass


def method_photoshop(img):
    assert img.shape[2]==4, "input is 4 channel img ,which contain alpha matting mask "
    return img[:,:,3]
