#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Abel Lee
# date: 2017
#Copyright: free

from django.db import models
import django.utils.timezone as timezone

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    real_name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=64)
    email = models.CharField(max_length=64, default='')
    phone = models.CharField(max_length=64, default='')
    description = models.CharField(max_length=256, default='')

    def __unicode__(self):
        return self.username

class Article(models.Model):
    article_id = models.CharField(max_length=128, primary_key=True)
    status = models.CharField(max_length=64)
    auther = models.CharField(max_length=64)
    htlm_context = models.TextField(default='')
    timestamp = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.article_id

class AtricleType(models.Model):
    type_id = models.CharField(max_length=128, primary_key=True)
    type_name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default='')

    def __unicode__(self):
        return self.type_id

class ArticleComment(models.Model):
    comment_id = models.CharField(max_length=128, primary_key=True)
    article_id = models.CharField(max_length=128)
    status = models.CharField(max_length=64)
    context = models.CharField(max_length=256, default='')
    timestamp = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.comment_id
