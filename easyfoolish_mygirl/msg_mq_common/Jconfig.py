'''
Created on Nov 16, 2018

@author: wangjian7
'''
import logging 

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.ERROR)

logger=logging.getLogger("s")
import os 

import yaml 
import os 
print (__file__)

config_data = yaml.load(open(os.path.join(os.path.dirname(__file__),"./config.yaml")))

import socket 
local_ip=socket.gethostbyname(socket.gethostname())

redis_server=config_data["redis"]["singleton"]["host"]
redis_port=config_data["redis"]["singleton"]["port"]



def _redis_handle():
#     redis_server_cluster=config_data["redis"]["cluster"]
#    import StrictRedisCluster
#    return StrictRedisCluster(startup_nodes=redis_server_cluster, skip_full_coverage_check=True,\
#                               decode_responses=False, socket_timeout=2, socket_connect_timeout=2)
    import redis
    return redis.StrictRedis(host=redis_server,port =redis_port, \
                              decode_responses=False, socket_timeout=2, socket_connect_timeout=2)

    
    
# class REDIS_KEY_CASE:
#     NOTIFY="notify"
#     ORIGIN="origin"
#     SAVE="save"
#     ERROR="error"

    
    
# def get_redis_key_v2(model_id,prefix="origin",is_queue=True,msg_id="",source_id=""):
#     if  model_id is None or not model_id   or model_id =="" :
#         #raise Exception("model_id is Null")
#         model_id="unknown"
#     def clear_illegal(w_str):
#         w_str=str(w_str) if w_str is not None else "unknown"
#         return w_str.replace(",","").replace(":","") if w_str is not None or w_str !="" else "unknown"
#     model_id=clear_illegal(model_id)
#     prefix=clear_illegal(prefix)
#     msg_id=clear_illegal(msg_id)
#     source_id= clear_illegal(source_id) if  clear_illegal(source_id)!="unknown" else msg_id
#     if is_queue:
#         prefix+="_img_q"
# 
#     build_="prefix:%s,model:%s"
#     if not is_queue :
#         #build_+=",source_id:%s,msg_id:%s"
#         build_+=",source_id:%s"
#         return build_%(prefix,model_id,source_id)
# 
#     return build_%(prefix,model_id)


    
# def parse_redis_key(key_str):
#     res=[x.split(":") for x in key_str.split(",")]
#     res_dict={}
#     for it in res:
#         if len(it)>1:
#             res_dict.update({it[0]:it[1]})
#     return res_dict


redis_handle=_redis_handle()

#EXPIRE_TIME=3600*24*30
EXPIRE_TIME=60*60
TIMEOUT_BPOP=5

BATCH_SIZE=16

daemon_time_sleep=1 ##10s


if __name__=="__main__":

    import unittest
    class build_t(unittest.TestCase):
        def testParse(self):
            input_x="prefix:origin_img_q,model:this_is_model_id"
            ret= parse_redis_key(input_x)
            self.assertEqual(ret["prefix"],"origin_img_q")
            input_x="prefix:origin_img_q,model:this_is_model_id,source_id:this_is_source_id,msg_id:this_is_unique_id"
            ret= parse_redis_key(input_x)
            self.assertEqual(ret["source_id"],"this_is_source_id")
        def testBuild(self):
            ret=get_redis_key_v2(prefix="origin",is_queue=True,msg_id="x",model_id="y",source_id="z")
            self.assertTrue(ret[-2:]==":y")
            
            ret=get_redis_key_v2(prefix="origin",is_queue=False,msg_id="x",model_id="y",source_id="z")
            print ret
            self.assertTrue("source_id:z" in ret )

            #with self.assertRaises(Exception) as context:
            #    ret=get_redis_key_v2(prefix="origin",is_queue=False,msg_id="x",model_id="",source_id="")
            #    self.assertTrue('model_id is Null' in context.exception)

            #with self.assertRaises(Exception) as context:
            #    ret=    _v2(prefix="origin",is_queue=False,msg_id="x",model_id=None,source_id=None)
            #    self.assertTrue('model_id is Null' in context.exception)

            ret=get_redis_key_v2(prefix="origin",is_queue=False,msg_id="x",model_id="",source_id="")
            self.assertTrue("model:unknown" in ret )
            ret=get_redis_key_v2(prefix="origin",is_queue=False,msg_id="x",model_id=None,source_id=None)
            self.assertTrue("model:unknown" in ret )

            #comma counter
            ret=get_redis_key_v2(prefix="origin",is_queue=False,msg_id="x,x",model_id="y:y",source_id="z\"z")
            self.assertEqual(ret.count(":"),3)
            self.assertEqual(ret.count(","),3-1)
            self.assertEqual(ret.count("\""),1)
    unittest.main()


