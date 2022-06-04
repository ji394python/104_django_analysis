# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Jobs(models.Model):
    # 要繼承models.Model，此為固定寫法
    # 創建character，最大長度為32，保存用戶數據
    # 此處migration後會出現在{app name}下的migration folder 作為紀錄
    # 此處的UserInfo，會被views給呼叫出來儲存用戶提交的東西 -> 參考views.py
    jobAnnounceDate = models.CharField(max_length=32, verbose_name="發布日期")
    jobTitles = models.CharField(max_length=1000, verbose_name="職缺名稱")
    jobCompanyName = models.CharField(max_length=32, verbose_name="公司名稱")
    jobCompanyUrl = models.CharField(max_length=32, verbose_name="公司連結")
    jobCompanyIndustry = models.CharField(max_length=32, verbose_name="產業類別")
    jobContent = models.CharField(max_length=100000, verbose_name="職缺內容")
    jobCategory = models.CharField(max_length=100, verbose_name="職位類別")
    jobSalary = models.CharField(max_length=32, verbose_name="薪資")
    jobLocation = models.CharField(max_length=32, verbose_name="工作地點")
    jobRqYear = models.CharField(max_length=32, verbose_name="年資要求")
    jobRqEducation = models.CharField(max_length=32, verbose_name="學歷要求")
    jobRqDepartment = models.CharField(max_length=32, verbose_name="科系要求")
    jobSpecialty = models.CharField(max_length=32, verbose_name="擅長工具")
    jobOthers = models.CharField(max_length=1000000, verbose_name="其他條件")
    jobDetailUrl = models.CharField(max_length=32, verbose_name="職缺連結")
    jiebaCut = models.CharField(
        max_length=1000000, verbose_name="職缺斷詞", null=True)
