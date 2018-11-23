'''
Created on Nov 15, 2018

@author: wangjian7
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import argparse
import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
import glob
import logging
import os
import sys
import time

#import redis_utils as util
import logging

from caffe2.python import workspace

from detectron.core.config import assert_and_infer_cfg
from detectron.core.config import cfg
from detectron.core.config import merge_cfg_from_file
from detectron.utils.io import cache_url
from detectron.utils.logging import setup_logging
from detectron.utils.timer import Timer
import detectron.core.test_engine as infer_engine
import detectron.datasets.dummy_datasets as dummy_datasets
import detectron.utils.c2 as c2_utils

#import detectron.utils.vis as vis_utils
import Dtron_vis as vis_utils

out_queue="detectron"
in_queue="detectron_result"
batch_size=1

from easyfoolish_mygirl.common import Jconfig
from easyfoolish_mygirl.common import mq_dataset
import yaml 
import numpy as np 


c2_utils.import_detectron_ops()

# OpenCL may be enabled by default in OpenCV3; disable it because it's not
# thread safe and causes unwanted GPU memory allocations.
cv2.ocl.setUseOpenCL(False)


class DtronImp:
    
    def __init__(self):

        pass 
    def listen (self,is_debug=True):

        currt =   os.path.dirname(os.path.abspath(__file__))
        l1 = "./config/args.yaml"
        l1 = os.path.join(currt,l1)

        ####################
        args=yaml.load(open(l1))
        self.args=args
        print (args)
        ######init  ops env 
        ####################
        
        self.logger = logging.getLogger(__name__)
        merge_cfg_from_file(args["cfg"])
        cfg.NUM_GPUS = 1
        weights = args["weights"]
        assert_and_infer_cfg(cache_urls=False)
        
        assert not cfg.MODEL.RPN_ONLY, \
        'RPN models are not supported'
        assert not cfg.TEST.PRECOMPUTED_PROPOSALS, \
        'Models that require precomputed proposals are not supported'
        
        self.model = infer_engine.initialize_model_from_cfg(weights)
        self.timers = defaultdict(Timer)

        #dummy_coco_dataset = dummy_datasets.get_coco_dataset()
        
        with c2_utils.NamedCudaScope(0):
        ####################
        ###### listen 
        ####################
            null_ct = 0
            while True :
                data_recv = self. _getdata()
                if data_recv is None or len(data_recv)<=0 :
                    if is_debug :
                        null_ct+=1 
                        if null_ct>100:
                            break
                    continue 
                self.logger.info(
                    ' \ Note:  find a image ,shape: '+str(data_recv[0][2].shape)
                )
                collect_list = []                
                for msg_id ,_, img  in data_recv:
                    matting = self._process(img)

                    collect_list.append( (msg_id,img,matting) )
                
                self._response(collect_list)
                self.logger.info(
                    ' \ Note:  send a image ,len: '+str(len(collect_list) ) +"  \ "
                )
                
    def _getdata (self):
        _,mq_name = mq_dataset.build_key(None, out_queue)
        data_list = mq_dataset.get_jobs(mq_name, job_batch_size=batch_size)
        if data_list is None or len(data_list) <=0:
            return []
        data_list = [ (msg_id, None ,data ) for msg_id ,data in data_list ]
        return data_list
    
    def _process (self,im):
        t = time.time()

        cls_boxes, cls_segms, cls_keyps = infer_engine.im_detect_all(
                self.model, im, None, timers=self.timers
            )
        
        self.logger.info('Inference time: {:.3f}s'.format(time.time() - t))
        for k, v in self.timers.items():
            self.logger.info(' | {}: {:.3f}s'.format(k, v.average_time))
        self.logger.info(
            ' \ Note: inference on the first image will be slower than the '
            'rest (caches and auto-tuning need to warm up)'
        )
        mask_list=vis_utils.vis_one_image_opencv_mask_list(
            im[:, :, ::-1],  # BGR -> RGB for visualization
            #im_name,
            #args.output_dir,
            cls_boxes,
            cls_segms,
            cls_keyps,
            dataset=None,
            #box_alpha=0.3,
            show_class=True,
            thresh=self.args["thresh"],
            kp_thresh=self.args["kp_thresh"],
            #ext=args.output_ext,
            #out_when_no_box=args.out_when_no_box
        )
        return np.array(mask_list )
    def _response(self, cl_list ):

        save_list = [] 
        for msg_id ,rgb, matting in cl_list:
            save_list.append( (msg_id,matting) )
        mq_dataset.intermediate_job_finish(in_queue,save_list)

def run_while():    
    workspace.GlobalInit(['caffe2', '--caffe2_log_level=3'])

    obj=DtronImp()
    obj.listen(is_debug=False)


if __name__=="__main__":
    import unittest
    import PIL.Image 
    import numpy as np 
    class xx(unittest.TestCase):
        def setUp(self):
            p="../../../images/2009_000237.jpg"
            img = PIL.Image .open(p).convert("RGB")
            img = np.array(img)
        
            ##mock data 
            save_list = [img] *13 
            mq_dataset.intermediate_job_finish(out_queue,save_list)
        
        
        def test_tf_seg(self):
            obj = DtronImp()
            
            ###init 
            obj.listen(is_debug=True)
    
    #unittest.main()
    
    
