#! -*- coding: utf-8 -*-

import tensorflow as tf
from PIL import Image
import os
import numpy as np
batch_size =8 

out_queue="portrait_seg_tf"
in_queue="merge_tf"

from easyfoolish_mygirl.msg_mq_common import Jconfig
from easyfoolish_mygirl.msg_mq_common import mq_dataset

sess,output,input_x =None ,None ,None



def normlize_item(origin_image_np):
    origin_image = Image.fromarray(origin_image_np,"RGB")
#         origin_width, origin_height = origin_image.size
    image = origin_image.resize((512, 512), Image.ANTIALIAS)
    width, height = image.size
    
    r_mean = 126.888888
    g_mean = 115.888888
    b_mean = 110.888888
    
    r_layer = np.array([r_mean] * height * width, dtype=np.float32)
    r_layer = np.reshape(r_layer, [height, width, 1])
    g_layer = np.array([g_mean] * height * width, dtype=np.float32)
    g_layer = np.reshape(g_layer, [height, width, 1])
    b_layer = np.array([b_mean] * height * width, dtype=np.float32)
    b_layer = np.reshape(b_layer, [height, width, 1])
    mean_image = np.concatenate((r_layer, g_layer, b_layer), axis=-1)
    
    image = np.array(image, dtype=np.float32)
    image = np.reshape(image, [512, 512, 3])
    
    image = (image - mean_image) / 255.0
    image = image[np.newaxis, ...]
    return image

    
def _get_data():
    _,mq_name = mq_dataset.build_key(None, out_queue)
    data_list = mq_dataset.get_jobs(mq_name, job_batch_size=batch_size)
    data_list = [ (msg_id, normlize_item(data),data ) for msg_id ,data in data_list ]
    return data_list


def _post_process(msg_ids,result_list,each_image_list):
    def format_img(result,each_image):
        origin_image = Image.fromarray(each_image).convert('RGB')
        origin_width, origin_height = origin_image.size
    
        result = result * 255
        result = np.array(result, dtype=np.uint8)
    
        matte_image = Image.fromarray(result, mode='L') \
            .resize([origin_width, origin_height], resample=Image.BILINEAR)
    #     matte_image_np=np.array(matte_image,dtype=np.uint8)
    
        p = Image.new('RGBA', [origin_width, origin_height], (0, 0,0))
        p.paste(origin_image, (0, 0, origin_width,origin_height), matte_image)
        p=p.convert("RGB")
        return np.array(p),np.array(matte_image)
        
    save_list = [] 
    for msg_id ,result,each_image in zip(msg_ids,result_list,each_image_list):
        rgb,matting = format_img(result,each_image)
        save_list.append( (msg_id,matting) )
    mq_dataset.intermediate_job_finish(in_queue,save_list)
 

     
def run_while(is_debug=False):
#     print type(origin_img_np),origin_img_np.shape
#     assert type(origin_img_np) == np.ndarray ,"expect input is ndarray,"
    global  sess,output,input_x

    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()
        output_graph_path = './checkpoint/frozen_model.pb'
    
    
        with open(output_graph_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")
    
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            input_x = sess.graph.get_tensor_by_name("input:0")
            raw_output = sess.graph.get_tensor_by_name("output:0")
    
            ##################################################################
            _, output = tf.split(raw_output, num_or_size_splits=2, axis=3)
            output = tf.squeeze(output)

            null_ct = 0 
            while True :
                data_recv =  _get_data()
                if data_recv is None or len(data_recv)<=0 :
                    if is_debug :
                        null_ct+=1 
                        if null_ct>100:
                            print ("null.. return ")
                            break
                    continue 
                msg_list,data_list,origin_list =  zip(*data_recv)
                print msg_list
                img = np.concatenate(data_list,axis=0)
                assert len(img.shape )==4 and img.shape[-1]==3 ,"expect n,w,h,c, but get "+str(img.shape)
                
                if img.shape[0]!=batch_size :
                    for i in range(batch_size-img.shape[0]):
                        item =  np.zeros(img.shape[1:],dtype=img[0].dtype)
                        item = np.expand_dims(item, axis=0)
                        img = np.concatenate([img,item] , axis=0)
                
                image = img [:batch_size]
                assert image.shape[0]==batch_size ,"expect n,w,h,c, but get "+str(image.shape)
                
                print "normlize...",msg_list,type(image),image.shape 
                result = sess.run(output, feed_dict={input_x: image})
    
                ################################################3
                print "result....",result.shape,len(result),len(data_list)
                print result[0].shape 
                print data_list[0].shape 
                
                residual_len=len(msg_list)
                _post_process(msg_list,result[:residual_len],origin_list[:residual_len])
                
    return None 

                
    

if __name__=="__main__":
    import unittest
    import PIL.Image 
    import numpy as np 
    class xx(unittest.TestCase):
        def setUp(self):
            p="./images/2009_000237.jpg"
            img = PIL.Image .open(p).convert("RGB")
            img = np.array(img)
        
            ##mock data 
            save_list = [img] *13 
            mq_dataset.intermediate_job_finish(out_queue,save_list)
        
        def test_tf_seg(self):
            ###init 
            run_while(is_debug=True)
    
    unittest.main()
    
    
                