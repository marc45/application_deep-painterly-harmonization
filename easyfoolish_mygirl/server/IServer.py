'''
Created on Nov 15, 2018

@author: wangjian7
'''

class IServer:
    redis_handle=None 
    
    def listen (self):
        raise Exception("not implement")
