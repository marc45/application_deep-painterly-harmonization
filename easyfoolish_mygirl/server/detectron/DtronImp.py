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

import redis_utils as util
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
import detectron.utils.vis as vis_utils


out_queue="detectron"
in_queue="detectron_result"

from easyfoolish_mygirl.msg_mq_common import Jconfig
from easyfoolish_mygirl.msg_mq_common import mq_dataset


c2_utils.import_detectron_ops()

# OpenCL may be enabled by default in OpenCV3; disable it because it's not
# thread safe and causes unwanted GPU memory allocations.
cv2.ocl.setUseOpenCL(False)

class DtronImp:
    
    def __init__(self):

        pass 
    def listen (self,is_debug=True):
        ####################
        ######init  ops env 
        ####################
        
        self.logger = logging.getLogger(__name__)
        merge_cfg_from_file(args.cfg)
        cfg.NUM_GPUS = 1
        weights = cfg.DOWNLOAD_CACHE
        assert_and_infer_cfg(cache_urls=False)
        
        assert not cfg.MODEL.RPN_ONLY, \
        'RPN models are not supported'
        assert not cfg.TEST.PRECOMPUTED_PROPOSALS, \
        'Models that require precomputed proposals are not supported'
        
        model = infer_engine.initialize_model_from_cfg(weights)
        dummy_coco_dataset = dummy_datasets.get_coco_dataset()
        
        with c2_utils.NamedCudaScope(0):
        ####################
        ###### listen 
        ####################
            null_ct = 0
            while True :
                data_recv = self. _getdata()
                if data_recv is None :
                    if is_debug :
                        null_ct+=1 
                        if null_ct>100:
                            print ("null.. return ")
                            break
                    continue 
                
                self._process(data_recv)
                
                self._response()
                
    def _getdata (self):
        _,mq_name = mq_dataset.build_key(None, out_queue)
        data_list = mq_dataset.get_jobs(mq_name, job_batch_size=batch_size)
        data_list = [ (msg_id, normlize_item(data),data ) for msg_id ,data in data_list ]
        return data_list
    
    def _process (self,im):
        cls_boxes, cls_segms, cls_keyps = self.infer_engine.im_detect_all(
                self.model, im, None, timers=self.timers
            )
        
        self.logger.info('Inference time: {:.3f}s'.format(time.time() - t))
        for k, v in self.timers.items():
            self.logger.info(' | {}: {:.3f}s'.format(k, v.average_time))
        self.logger.info(
            ' \ Note: inference on the first image will be slower than the '
            'rest (caches and auto-tuning need to warm up)'
        )
        img=vis_utils.vis_one_image_opencv(
            im[:, :, ::-1],  # BGR -> RGB for visualization
            #im_name,
            #args.output_dir,
            cls_boxes,
            cls_segms,
            cls_keyps,
            dataset=None,
            #box_alpha=0.3,
            show_class=True,
            thresh=args.thresh,
            kp_thresh=args.kp_thresh,
            #ext=args.output_ext,
            #out_when_no_box=args.out_when_no_box
        )
        return img 
    def _response(self,im ):
        img_return =self._process(im)
        util.send(key,  util.encode(msg)  )
        return key

    

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
            obj = DtronImp()
            
            ###init 
            obj.listen(is_debug=True)
    
    unittest.main()
    
    