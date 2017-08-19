#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:abellee
#date: 2017
#Copyright: free

import os
import django
from common.password import create_hashed_password
from admin.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

def init_user():
    User.objects.get_or_create(username='abellee',password=create_hashed_password('123456'),real_name='Abel Lee',role='admin')
    User.objects.get_or_create(username='user',password=create_hashed_password('123456'),real_name='user',role='user')

def init_article_type():
    pass

init_user()
