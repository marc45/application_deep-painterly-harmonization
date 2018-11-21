#! -*- coding: utf-8 -*-

#from PIL import Image
import cv2
import os
import numpy as np
import time
batch_size =8 

out_queue="transfer"
in_queue="transfer_result"

from easyfoolish_mygirl.msg_mq_common import Jconfig
from easyfoolish_mygirl.msg_mq_common import mq_dataset

out_save= "./listen/data_listen"
listen_dir="./listen/result_listen"


def __init__env():
    if not os.path.isdir(os.path.dirname(out_save)):
        os.mkdir(os.path.dirname(out_save))
    if not os.path.isdir(out_save):
        os.mkdir(out_save)
    if not os.path.isdir(listen_dir):
        os.mkdir(listen_dir)

__init__env()

def _get_data():
    _,mq_name = mq_dataset.build_key(None, out_queue)
    data_list = mq_dataset.get_jobs(mq_name, job_batch_size=batch_size)
    data_list = [ (msg_id, None ,data ) for msg_id ,data in data_list ]
    return data_list
def _process(data_list):
    #data is combine [navice ,mask1.mask2 ,backgrd] 
    #cmd_list = []
    for msg_id_c , _ , data in data_list :
        msg_id,_ =mq_dataset.build_key(msg_id_c,"tmp")
        msg_id= msg_id.replace("type:image,job:tmp,source_id:","")
        fn_1_list= [ os.path.join( out_save,msg_id+"_"+x )  for x in ["c_mask.jpg","c_mask_dilated.jpg","naive.jpg","target.jpg"]  ] 

        x1 = 0 
        for fn in fn_1_list :
            data_x = data[x1:x1+1]
            assert data_x.shape[3]==3 
            cv2.imwrite(fn,data_x)
            x1 += 1

def _listen_result_exist():
    def _post_process(info_):
        msg_id ,info_path = info_ 
        if os.path.isfile(info_path):
            data = cv2.imread(info_path)
            msg_id_new = mq_dataset.build_key(msg_id , in_queue)
            info_x=(msg_id_new,data)
            msg_save_list = mq_dataset.intermediate_job_finish(in_queue, [info_x] )
    ##scan ....
    #0_final_res.jpg
    ls_list = [ (x.replace("_final_res.jpg","") ,os.path.join(listen_dir,x) ) for x in os.listdir(listen_dir) ]
    #[msg_id ,path ]
    for msg_id,path_info   in ls_list :
        
        msg_id_redis = mq_dataset.build_key(msg_id,in_queue) 
        if not Jconfig.redis_handle.exists(msg_id_redis) :
            _post_process((msg_id,path_info))

 

     
def run_while(is_debug=False):
    while True :
        _listen_result_exist()
        data_recv =  _get_data()
        if data_recv is None or len(data_recv)<=0 :
            _process(data_recv)
                
        time.sleep(0.5)

                
    
#if __name__=="__main__":
#    run_while()
if __name__=="__main__":
    import unittest
    import numpy as np 
    def create():
        img=(np.random.randn(10,10,3)*255).astype(np.uint8)
        return img
    class xx(unittest.TestCase):
        def setUp(self):
            global out_queue,in_queue,out_save,listen_dir 

            out_queue="unittest_transfer"
            in_queue="unittest_transfer_result"

            out_save= "./unittest_listen/data_listen"
            listen_dir="./unittest_listen/result_listen"
            self.tearDown()


            if not os.path.isdir(os.path.dirname(out_save)):
                os.mkdir(os.path.dirname(out_save))
            if not os.path.isdir(out_save):
                os.mkdir(out_save)
            if not os.path.isdir(listen_dir):
                os.mkdir(listen_dir)



            data_list= []
            for i in range(batch_size):
                mock_data = [create()]*4  
                data_list.append(   np.array(mock_data) )
            self.msg_list = []
            self.msg_list = mq_dataset.intermediate_job_finish(out_queue, data_list )

            for i,(x,y) in enumerate(self.msg_list  ):
                x=x.replace("type:image,job:unittest_transfer,source_id:","")
                fn=os.path.join(listen_dir,x+"_final_res.jpg")
                da= create () 
                cv2.imwrite(fn,da)

        
        def test_01__process(self):
            data_list = _get_data()
            _process(data_list)

            return_msg_id= [os.path.basename(x) for x,y in self.msg_list ]
            return_msg_id=sorted(return_msg_id)

            scan_list = os.listdir(out_save) 
            aa_msg_id= ["type:image,job:unittest_transfer,source_id:"+os.path.basename(y).replace("_naive.jpg","") for y in scan_list if "_naive" in y ]
            aa_msg_id=sorted(aa_msg_id)
            print "========"*4
            print aa_msg_id,return_msg_id
            print "========"*4
            self.assertTrue(set(aa_msg_id)==set(return_msg_id))

        def test_02_listen_result_exist(self):
            _listen_result_exist()
            ###
            ## assert save success 
            for msg_id in self. msg_list :
                msg_id_redis,_ = mq_dataset.build_key(msg_id,in_queue)
                print msg_id_redis 
                self.assertTrue(Jconfig.redis_handle.exists(msg_id_redis))


        def tearDown(self):
            keys =Jconfig.redis_handle.keys()
            keys = [x for x in keys if "type:image,job:unittest_transfer" in x ]

            keys.append("type:mq,job:unittest_transfer")
            keys.append("type:mq,job:unittest_transfer_result")

            for k in keys :
                Jconfig.redis_handle.delete(k)
            import shutil 
            self.image_list = []
            if os.path.isdir("./unittest_listen"):
                shutil.rmtree("./unittest_listen")


            
    unittest.main()
    
    
                

