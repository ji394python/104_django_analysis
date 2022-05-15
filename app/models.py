# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserInfo(models.Model):
    # 要繼承models.Model，此為固定寫法
    # 創建character，最大長度為32，保存用戶數據
    # 此處migration後會出現在{app name}下的migration folder 作為紀錄
    # 此處的UserInfo，會被views給呼叫出來儲存用戶提交的東西 -> 參考views.py
    title = models.CharField(max_length=32)
    line = models.CharField(max_length=32)
    price = models.CharField(max_length=32)
    booking_date = models.CharField(max_length=32)
    star = models.CharField(max_length=32)
