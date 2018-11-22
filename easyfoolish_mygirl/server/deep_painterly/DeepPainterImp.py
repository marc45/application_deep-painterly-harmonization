#! -*- coding: utf-8 -*-

#from PIL import Image
import cv2
import os
import numpy as np
import time
batch_size =8 

out_queue="transfer"
in_queue="transfer_result"

from easyfoolish_mygirl.common import Jconfig
from easyfoolish_mygirl.common import mq_dataset

scan_dir= "./listen/data_listen"
save_dir="./listen/result_listen"


def __init__env():
    if not os.path.isdir(os.path.dirname(scan_dir)):
        os.mkdir(os.path.dirname(scan_dir))
    if not os.path.isdir(scan_dir):
        os.mkdir(scan_dir)
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

__init__env()

def _get_data():
    _,mq_name = mq_dataset.build_key(None, out_queue)
    data_list = mq_dataset.get_jobs(mq_name, job_batch_size=batch_size)
    if data_list is None or len(data_list)<=0 :
        return []
    data_list = [ (msg_id, None ,data ) for msg_id ,data in data_list ]
    return data_list
def _process(data_list):
    #data is combine [navice ,mask1.mask2 ,backgrd] 
    #cmd_list = []
    for msg_id_c , _ , data in data_list :
        msg_id,_ =mq_dataset.build_key(msg_id_c,"tmp")
        msg_id= msg_id.replace("type:image,job:tmp,source_id:","")
        fn_1_list= [ os.path.join( scan_dir,msg_id+"_"+x )  for x in ["c_mask.jpg","c_mask_dilated.jpg","naive.jpg","target.jpg"]  ] 

        x1 = 0 
        print ("total find ..",len(fn_1_list),data.shape)
        for fn in fn_1_list :
            data_x = data[x1:x1+1]
            assert len(data_x.shape)==4 
            data_x=np.squeeze(data_x,axis=0)
            assert data_x.shape[2]==3 
            cv2.imwrite(fn,data_x)
            x1 += 1

def _listen_result_exist():
    def _post_process(msg_id,info_path):
        if os.path.isfile(info_path):
            data = cv2.imread(info_path)
            info_x=(msg_id,data)
            msg_save_list = mq_dataset.intermediate_job_finish(in_queue, [info_x] )
    ##scan ....
    #0_final_res.jpg
    ls_list = [ (x.replace("_final_res.jpg","") ,os.path.join(save_dir,x) ) for x in os.listdir(save_dir) ]
    #[msg_id ,path ]
    for msg_id,path_info   in ls_list :
        
        msg_id_redis,_ = mq_dataset.build_key(msg_id,in_queue) 
        if not Jconfig.redis_handle.exists(msg_id_redis) :
            _post_process(msg_id_redis,path_info)

     
def run_while(is_debug=False):
    while True :
        _listen_result_exist()
        data_recv =  _get_data()
        if data_recv is None or len(data_recv)<=0 :
            time.sleep(0.5)
            continue
        _process(data_recv)





                
    
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
            global out_queue,in_queue,scan_dir,save_dir 

            out_queue="unittest_transfer"
            in_queue="unittest_transfer_result"

            scan_dir= "./unittest_listen/data_listen"
            save_dir="./unittest_listen/result_listen"
            self.tearDown()


            if not os.path.isdir(os.path.dirname(scan_dir)):
                os.mkdir(os.path.dirname(scan_dir))
            if not os.path.isdir(scan_dir):
                os.mkdir(scan_dir)
            if not os.path.isdir(save_dir):
                os.mkdir(save_dir)



            data_list= []
            for i in range(batch_size):
                mock_data = [create()]*4  
                data_list.append(   np.array(mock_data) )
            self.msg_list = []
            self.msg_list = mq_dataset.intermediate_job_finish(out_queue, data_list )

            for i,(x,y) in enumerate(self.msg_list  ):
                x=x.replace("type:image,job:unittest_transfer,source_id:","")
                fn=os.path.join(save_dir,x+"_final_res.jpg")
                da= create () 
                cv2.imwrite(fn,da)

        
        def test_01__process(self):
            data_list = _get_data()
            _process(data_list)

            return_msg_id= [os.path.basename(x) for x,y in self.msg_list ]
            return_msg_id=sorted(return_msg_id)

            scan_list = os.listdir(scan_dir) 
            aa_msg_id= ["type:image,job:unittest_transfer,source_id:"+os.path.basename(y).replace("_naive.jpg","") for y in scan_list if "_naive" in y ]
            aa_msg_id=sorted(aa_msg_id)
            self.assertTrue(set(aa_msg_id)==set(return_msg_id))

        def test_02_listen_result_exist(self):
            _listen_result_exist()
            ###
            #build disk fn 
            exist_list = [os.path.basename(x) for x in  os.listdir(save_dir) ]
            build_list = [ x.split("source_id:") [-1] + "_final_res.jpg"   for x,_ in self.msg_list]

            self.assertTrue(set(exist_list)==set(build_list))
            ## assert save success 
            for msg_id,_ in self. msg_list :
                msg_id_redis,_ = mq_dataset.build_key(msg_id,in_queue)
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
            #if os.path.isdir("./unittest_listen"):
            #    shutil.rmtree("./unittest_listen")


            
    unittest.main()
    
    
                

