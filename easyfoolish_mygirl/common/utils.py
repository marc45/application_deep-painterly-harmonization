# '''
# Created on Nov 15, 2018
# 
# @author: wangjian7
# '''
# 
# from common import  caffe2_pb2 
# import numpy as np 
# 
#   
# def encode_msg(msg):
#     # Create TensorProtos
#     print "encode--------.....>",msg.shape
#     msg = msg.astype( np.uint8)
#     tensor_protos = caffe2_pb2.TensorProtos()
#     img_tensor = tensor_protos.protos.add()
#     img_tensor.dims.extend(msg.shape)
#     img_tensor.data_type = 4
#     img_tensor.name = str(msg.shape)
#     flatten_img = msg.reshape(np.prod(msg.shape))
#     img_tensor.name = str(msg.shape)+"----"+str(flatten_img.shape)
# 
#     img_tensor.string_data.append(flatten_img.tostring())
#     
#     return tensor_protos.SerializeToString()
# 
# def decode_msg(databuf):
#     tensor_protos = caffe2_pb2.TensorProtos()
#     tensor_protos.ParseFromString(databuf)
#     img_proto=tensor_protos.protos[0]
#     imgbuf=img_proto.string_data[0]
#     dataArray = np.frombuffer(imgbuf, np.uint8)
#     
#     dataArray=dataArray.reshape(img_proto.dims)
#     print "decode........------>",dataArray.shape
#     return dataArray

