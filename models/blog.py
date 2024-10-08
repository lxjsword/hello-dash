#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   user.py
@Time    :   2024/09/23 11:41:23
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import datetime
import peewee

from db import db 
from log import log_info, log_error


class Blog(peewee.Model):

    class Meta:
        database = db
        table_name = 't_blog'

    id = peewee.BigIntegerField(primary_key=True)
    title = peewee.CharField()
    tags = peewee.CharField()
    path = peewee.CharField()
    creator = peewee.CharField(max_length=20, default='admin')
    create_time = peewee.DateTimeField(default=datetime.datetime.now)
    last_modify_time = peewee.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def update(cls, *args, **kwargs):
        kwargs['last_modify_time'] = datetime.datetime.now()
        return super(Blog, cls).update(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.last_modify_time = datetime.datetime.now()
        return super(Blog, self).save(*args, **kwargs)
    

class BlogTag(peewee.Model):

    class Meta:
        database = db
        table_name = 't_blog_tag'

    id = peewee.BigIntegerField(primary_key=True)
    tag_name = peewee.CharField()
    creator = peewee.CharField(max_length=20, default='admin')
    create_time = peewee.DateTimeField(default=datetime.datetime.now)
