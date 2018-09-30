from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
from . import managers
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    post_level = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = managers.UserManager()
    def __str__(self):
        return self.username
class Posts(models.Model):
    page = models.ForeignKey('Users', on_delete=models.CASCADE, default=None)
    content = models.TextField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = managers.PostManager()

class Comments(models.Model):
    comment = models.TextField(max_length=1024) 
    post_id = models.ForeignKey('Posts', on_delete=models.CASCADE, default=None )
    user = models.ForeignKey('Users', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = managers.CommentManager()

