# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from .forms import NameForm
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .scrappers import Scrape_104
from .models import *
import pandas as pd
from .jieba_cut import Jieba_Cut


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        print(load_template)

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        if load_template == 'ui-tables.html':
            if request.method == 'POST':
                continue
                search = request.POST.get('search')
                S104 = Scrape_104('實習 intern', 150)
                S104 = S104.scrape()
                cut = Jieba_Cut(S104, r'app\doc\stopword.txt',
                                r'app\doc\user.txt')  # 斷詞模組
                cut.cut()
                # 0516: SQLite在heroku會有問題，故改用csv
                for r, i in S104.iterrows():
                    jobAnnounceDate = str(i['jobAnnounceDate'])
                    jobTitles = str(i['jobTitles'])
                    jobCompanyName = str(i['jobCompanyName'])
                    jobCompanyUrl = str(i['jobCompanyUrl'])
                    jobCompanyIndustry = str(i['jobCompanyIndustry'])
                    jobContent = str(i['jobContent'])
                    jobCategory = str(i['jobCategory'])
                    jobSalary = str(i['jobSalary'])
                    jobLocation = str(i['jobLocation'])
                    jobRqYear = str(i['jobRqYear'])
                    jobRqEducation = str(i['jobRqEducation'])
                    jobRqDepartment = str(i['jobRqDepartment'])
                    jobSpecialty = str(i['jobSpecialty'])
                    jobOthers = str(i['jobOthers'])
                    jobDetailUrl = str(i['jobDetailUrl'])
                    jiebaCut = str(i['jiebaCut'])
                    Jobs.objects.create(jobAnnounceDate=jobAnnounceDate,
                                        jobTitles=jobTitles,
                                        jobCompanyName=jobCompanyName,
                                        jobCompanyUrl=jobCompanyUrl,
                                        jobCompanyIndustry=jobCompanyIndustry,
                                        jobContent=jobContent,
                                        jobCategory=jobCategory,
                                        jobSalary=jobSalary,
                                        jobLocation=jobLocation,
                                        jobRqYear=jobRqYear,
                                        jobRqEducation=jobRqEducation,
                                        jobRqDepartment=jobRqDepartment,
                                        jobSpecialty=jobSpecialty,
                                        jobOthers=jobOthers,
                                        jobDetailUrl=jobDetailUrl,
                                        jiebaCut=jiebaCut)
                    print(f'{r}:新增資料')
                # print('成功新增資料')

                for row in Jobs.objects.all().reverse():
                    if Jobs.objects.filter(jobTitles=row.jobTitles).count() > 1:
                        row.delete()
                        # print('刪除資料')
            job_list = Jobs.objects.all()
            # django-filters
            # from .filters import JobFilter
            # jobFilter = JobFilter(queryset=job_list)
            # if request.method == "POST":
            #     jobFilter = JobFilter(request.POST, queryset=job_list)

            # django-tables2： pagination
            from .tables import jobsTable
            from django_tables2 import RequestConfig
            table = jobsTable(job_list)
            table.order_by = "-jobAnnounceDate"
            RequestConfig(request, paginate={"per_page": 20}).configure(table)

            context['table'] = table
            context["jobs"] = job_list
            context["tt"] = '職缺標題'
        if load_template == 'charts-morris.html':
            from pyecharts.charts import WordCloud, Bar
            from pyecharts import options as opts
            data = [
                ("生活", "999"),
                ("供热", "888"),
                ("供量", "777"),
                ("生活用水管理", "688"),
                ("供水", "588"),
                ("交通", "516"),
                ("城市", "515"),
                ("環保", "483"),
                ("房地管理", "462"),
                ("建设", "449"),
                ("保障", "429"),
                ("社會", "407"),
                ("發展", "254"),
                ("職缺", "254"),
                ("Python", "253"),
                ("R", "253"),
                ("SQL", "223"),
                ("Java", "223"),
                ("Hardoop", "223"),
                ("Spart", "223"),
                ("UDST", "152"),
                ("TWD", "152"),
                ("脫鉤", "152"),
                ("經濟", "152"),
                ("專案", "112"),
                ("怒", "112"),
                ("開心", "112"),
                ("哈哈哈哈哈", "92"),
                ("煩死了", "92"),
                ("管理", "92"),
                ("文娱", "72"),
                ("秩序", "72"),
                ("啟發", "72"),
                ("NP-P", "72"),
                ("占道", "71"),
                ("地上", "71"),
                ("健身", "41"),
                ("排放", "41"),
                ("資料庫", "41"),
                ("財報", "41"),
                ("???", "41")
            ]

            x = (
                WordCloud()
                .add(series_name="文字雲", data_pair=data, word_size_range=[6, 66])
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="文字雲", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=True),
                )
                .render_embed()
            )
            context['plot_div'] = x
            c = (
                Bar(init_opts=opts.InitOpts(width="300px",
                                            height="300px",
                                            page_title="柱狀圖")
                    )
                .add_xaxis(["A", "B", "C", "D", "E", "F"])
                .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
                .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
                .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本範例", subtitle="副標題")).render_embed()
            )
            context['bar'] = c

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
