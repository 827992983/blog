#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: Abel Lee
#date: 2017
#Copyright: free

import bcrypt

def create_hashed_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def check_password(password, hashed):
    try:
        return (bcrypt.hashpw(password, hashed) == hashed)
    except Exception, e:
        print('check password failed. [%s]' % (e))
        return False
