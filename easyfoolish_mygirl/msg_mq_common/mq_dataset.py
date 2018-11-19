'''
Created on Nov 19, 2018

@author: wangjian7
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# from rq import Connection, Queue, Worker

from easyfoolish_mygirl.msg_mq_common import Jconfig
from easyfoolish_mygirl.msg_mq_common import caffe2_pb2

import numpy as np 
import hashlib 
import PIL.Image 
pipline_list =["origin","setp1","setp2","step3.1","step3.2","step4"]

def build_key(source_id=None,model=None):
    source_id =str(source_id)
    def parse (infostr):
        if ":" not in infostr :
            return  {"source_id":infostr}
        type_str,model_str,source_id=None,None ,None
        dict_data = {}
        for data in infostr.split(",") :
            if "type:" in data :
                type_str=data.replace("type:","").strip()
                dict_data.update({"type":type_str})
            if "job:" in data :
                model_str=data.replace("job:","").strip()
                dict_data.update({"job":model_str})
            if "source_id:" in data :
                id_str=data.replace("source_id:","").strip()
                dict_data.update({"source_id":id_str})

        return dict_data
#         return {"type":type_str,"job":model_str,"source_id":id_str}
    bak_source_id=source_id
    
    dict_data=parse(source_id)
    source_id=dict_data.get("source_id",None)
    if source_id is None :
        raise Exception("illegal source_id,,,,,"+bak_source_id)
    
    model = model.replace(",","").replace(":","") if model is not None else None 
    if model is None :
        model = dict_data.get("job",model)

    sorted_key={"type":0,"job":1,"source_id":2}
    
    dict_data .update({"type":"image","job":model,"source_id":source_id})
    dict_data_items = sorted(dict_data.items(),key=lambda kv:sorted_key.get(kv[0]) )        
    dict_str = ",".join([str(x)+":"+str(y) for x,y in  dict_data_items ] )
    
    dict_data_mq ={"type":"mq","job":model}
    dict_data_items = sorted(dict_data_mq.items(),key=lambda kv:sorted_key.get(kv[0]) )        
    dict_mq_str = ",".join([str(x)+":"+str(y) for x,y in  dict_data_items ] )
    
    return  dict_str,dict_mq_str

def encode_msg(msg):
    if msg  is None :
        return None
    # Create TensorProtos
    msg = msg.astype( np.uint8)
    tensor_protos = caffe2_pb2.TensorProtos()
    img_tensor = tensor_protos.protos.add()
    img_tensor.dims.extend(msg.shape)
    img_tensor.data_type = 4
    img_tensor.name = str(msg.shape)
    flatten_img = msg.reshape(np.prod(msg.shape))
    img_tensor.name = str(msg.shape)+"----"+str(flatten_img.shape)

    img_tensor.string_data.append(flatten_img.tostring())
    
    return tensor_protos.SerializeToString()

def decode_msg(databuf):
    if databuf  is None :
        return None
    tensor_protos = caffe2_pb2.TensorProtos()
    tensor_protos.ParseFromString(databuf)
    img_proto=tensor_protos.protos[0]
    imgbuf=img_proto.string_data[0]
    dataArray = np.frombuffer(imgbuf, np.uint8)
    
    dataArray=dataArray.reshape(img_proto.dims)
    return dataArray

def hex_data(img_binary):
    def _is_pil_image(img):
        return isinstance(img, PIL.Image.Image)
    
    if _is_pil_image(img_binary):
        return hashlib.md5(np.array(img_binary,np.uint8)).hexdigest()

    a=np.asarray(img_binary, order='C')
    return hashlib.md5(a).hexdigest()


def get_jobs(mq_name,job_batch_size=1):
    mq_list = []
    data_list = []
    
    for i in range(job_batch_size):
        data = Jconfig.redis_handle.lpop(mq_name)
        print ("sacne...",mq_name)
        if data is None :
            continue 
        mq_list.append(data)
    for msg_id in mq_list : 
        data = Jconfig.redis_handle.get(msg_id)
        data = decode_msg(data)
        if data is None :
            continue
        data_list.append(( msg_id,data) )
    ##parse 
    return data_list 
#     if job_batch_size >1 :
#         raise Exception ("not support batch ,will be implemented in future  ")


def intermediate_job_finish(mq_name,data_list=[]):
    '''
    param data_list :
        [(msg_id,data)]
        [data]
    '''
    if len(data_list)<=0 :
        return None 
    if type(data_list[0]) !=tuple :
        data_list = [( hex_data(x),x)  for x in data_list ]
        
    data_list_encode = [(build_key(msg_id,mq_name), encode_msg(msg) ) for msg_id , msg in data_list]
    
    for (msg_str,mq_str),data in data_list_encode:
        is_cess = Jconfig.redis_handle.set(msg_str,data,Jconfig.EXPIRE_TIME)
        if is_cess  :        
            Jconfig.redis_handle.rpush(mq_str,msg_str)
    return [x for x,y  in data_list_encode ]
#     if job_batch_size >1 :
#         raise Exception ("not support batch ,will be implemented in future  ")



if __name__=="__main__":
    import unittest 
    class dataset(unittest.TestCase):
        mq_list = []
        
        def test_build_key(self):
            str2,str1= build_key("1234567","unittest_m1")
            self.mq_list.append(str1)
            print (str1,str2)
            self.assertTrue("unittest_m1" in str1 )
            self.assertTrue("source_id:123456" in str2 )
            
            
            str2,str1= build_key("job:m2,type:mq,source_id:123456","unittest_m2xxx")
            self.mq_list.append(str1)
            print (str1,str2)
            self.assertTrue("unittest_m2" in str1 )
            self.assertTrue("type:mq" in str1 )
            self.assertTrue("source_id:123456" in str2 )
            
            pass 
        def test_save(self):
            out_q_list=["unittest_up1","unittest_up2","unittest_up3"]
        
            for nm in out_q_list:
                data_list = (np.random.randn(4,10,10,3)*255).astype(np.uint8)
                data_list = data_list.tolist()
                data_list = [np.array(x) for x in data_list ]
                name_list = intermediate_job_finish(nm,data_list)
            
                self.mq_list.extend([mq_str for x,mq_str in name_list ] )
            
        def tearDown(self):
            print (set(self.mq_list))
            ###pop 
            for mq in self.mq_list:
                item =get_jobs(mq,16)
                while item is not None  and len(item)>0 :
                    item =get_jobs(mq,16)
                    print (len(item))
                    pass
    
    unittest.main()
    ##mock 
    # Range of Fibonacci numbers to compute
    # Kick off the tasks asynchronously
    
#         print (type(items),items)
#     print (dir(items))