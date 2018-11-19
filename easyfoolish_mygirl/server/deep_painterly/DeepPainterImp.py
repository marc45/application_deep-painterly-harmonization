# '''
# Created on Nov 15, 2018
# 
# @author: wangjian7
# '''
# class DeepPainterImp:
#     q_mq_key="mq_paint_"
#     q_ref_key_prefix="origin_"
#     q_process_key_prefix="step02_"
#     
#     q_mq_timeout=2
#     def listen (self):
#                   
#         while True :
#             item,key_ref = self. redis_queue_fetch()
#             if item is None :
#                 continue
#             ##set batch_size 
#             ## if len(data)<batch_size :  data.append(item)
#             
#             self.response(item)    
#     
#     def response (self):
#         raise Exception("not implement")
# #     def redis_queue_fetch (self):
# #         raise Exception("not implement")
#     
#     
#     def _process (self,im):
#         cls_boxes, cls_segms, cls_keyps = self.infer_engine.im_detect_all(
#                 self.model, im, None, timers=self.timers
#             )
#         
#         self.logger.info('Inference time: {:.3f}s'.format(time.time() - t))
#         for k, v in self.timers.items():
#             self.logger.info(' | {}: {:.3f}s'.format(k, v.average_time))
#         self.logger.info(
#             ' \ Note: inference on the first image will be slower than the '
#             'rest (caches and auto-tuning need to warm up)'
#         )
#         img=vis_utils.vis_one_image_opencv(
#             im[:, :, ::-1],  # BGR -> RGB for visualization
#             #im_name,
#             #args.output_dir,
#             cls_boxes,
#             cls_segms,
#             cls_keyps,
#             dataset=None,
#             #box_alpha=0.3,
#             show_class=True,
#             thresh=args.thresh,
#             kp_thresh=args.kp_thresh,
#             #ext=args.output_ext,
#             #out_when_no_box=args.out_when_no_box
#         )
#         return img 
# if __name__=="__main__":
#     pass