# Generated by Django 3.2.13 on 2022-06-03 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220604_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='jobAnnounceDate',
            field=models.CharField(max_length=32, verbose_name='發布日期'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobCategory',
            field=models.CharField(max_length=100, verbose_name='職位類別'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobCompanyIndustry',
            field=models.CharField(max_length=32, verbose_name='產業類別'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobCompanyName',
            field=models.CharField(max_length=32, verbose_name='公司名稱'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobCompanyUrl',
            field=models.CharField(max_length=32, verbose_name='公司連結'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobContent',
            field=models.CharField(max_length=100000, verbose_name='職缺內容'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobDetailUrl',
            field=models.CharField(max_length=32, verbose_name='職缺連結'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobLocation',
            field=models.CharField(max_length=32, verbose_name='工作地點'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobOthers',
            field=models.CharField(max_length=1000000, verbose_name='其他條件'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobRqDepartment',
            field=models.CharField(max_length=32, verbose_name='科系要求'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobRqEducation',
            field=models.CharField(max_length=32, verbose_name='學歷要求'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobRqYear',
            field=models.CharField(max_length=32, verbose_name='年資要求'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobSalary',
            field=models.CharField(max_length=32, verbose_name='薪資'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobSpecialty',
            field=models.CharField(max_length=32, verbose_name='擅長工具'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobTitles',
            field=models.CharField(max_length=1000, verbose_name='職缺名稱'),
        ),
    ]