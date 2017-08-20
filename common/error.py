#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Abel Lee
#date: 2017
#Copyright: free

class Error(object):
    def __init__(self, code, msg=None, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def __str__(self):
        err = self.to_dict()
        return str(err)
    
    def to_dict(self):
        err = {}
        err['err_code'] = self.code
        if self.msg:
            err['err_msg'] = self.msg
        if self.data:
            err['data'] = self.data

        return err
    
    def err_code(self):
        return self.code
    
    def err_msg(self):
        return self.msg

def return_error(err, data=""):
    return {"ret_code": err.err_code(),
            "ret_msg": err.err_msg(),
            "data": data}

def return_success(data=""):
    return {"ret_code": 0,
            "ret_msg": "succeed",
            "data": data}