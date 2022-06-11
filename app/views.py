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
from .draw import *
from .tables import jobsTable
from django_tables2 import RequestConfig


@login_required(login_url="/login/")
def index(request):
    context = {}
    if request.method == 'POST':
        '''
            因伺服器我是免費版xD，故僅爬取七頁的職缺做更新，
            Default：沒輸入字的話，就是更新實習的職缺
        '''
        search = request.POST.get('search')
        S104 = Scrape_104(search, 7)
        S104 = S104.scrape()
        if search == '':
            search = '實習 intern'
        cut = Jieba_Cut(S104)  # 斷詞模組
        cut.cut(r'app/doc/stopword.txt', r'app/doc/user.txt')  # 停用詞與加權詞
        S104 = cut.df
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
            jobType = str(i['jobType'])
            jobApplyNums = str(i['jobApplyNums'])
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
                                jiebaCut=jiebaCut,
                                jobType=jobType,
                                jobApplyNums=jobApplyNums)
            print(f'{r}:新增資料')
        # print('成功新增資料')

        for row in Jobs.objects.all().reverse():
            if Jobs.objects.filter(jobTitles=row.jobTitles).count() > 1:
                row.delete()
    job_list = Jobs.objects.all()

    # django-tables2： pagination
    from .tables import jobsTable
    from django_tables2 import RequestConfig
    table = jobsTable(job_list)
    table.order_by = "-jobAnnounceDate"
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    context['table'] = table
    context["jobs"] = job_list
    context["tt"] = '職缺標題'

    html_template = loader.get_template('ui-tables.html')
    
    
    from .export import TableExport
    export_format = request.GET.get('_export', None)

    if TableExport.is_valid_format(export_format):
        from .tables import jobsTable2
        tablee = jobsTable2(job_list)
        table = tablee
        exporter = TableExport(export_format, table)
        return exporter.response('File_Name.{}'.format(export_format))
    
    
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        print(load_template)
        industry = ['data-engineer.html', 'data-analysis.html', 'marketing.html',
                    'administration.html', 'art-design.html', 'catering.html',
                    'service.html', 'technician.html', 'education.html']
        name = ['資訊工程', '數據分析', '行銷企劃', '行政助理',
                '藝術設計', '餐飲', '服務', '技術與操作', '教育']
        jobN = ['資訊工程', '數據分析', '行銷企劃', '行政事務',
                '媒體設計', '餐飲飯店', '服務業人員', '一般技術', '教育補教']

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        if load_template == 'ui-tables.html':
            if request.method == 'POST':
                '''
                    因伺服器我是免費版xD，故僅爬取七頁的職缺做更新，
                    Default：沒輸入字的話，就是更新實習的職缺
                '''
                search = request.POST.get('search')
                S104 = Scrape_104(search, 7)
                S104 = S104.scrape()
                if search == '':
                    search = '實習 intern'
                cut = Jieba_Cut(S104)  # 斷詞模組
                cut.cut(r'app/doc/stopword.txt',
                        r'app/doc/user.txt')  # 停用詞與加權詞
                S104 = cut.df
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
                    jobType = str(i['jobType'])
                    jobApplyNums = str(i['jobApplyNums'])
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
                                        jiebaCut=jiebaCut,
                                        jobType=jobType,
                                        jobApplyNums=jobApplyNums)
                    print(f'{r}:新增資料')
                # print('成功新增資料')

                for row in Jobs.objects.all().reverse():
                    if Jobs.objects.filter(jobTitles=row.jobTitles).count() > 1:
                        row.delete()
            job_list = Jobs.objects.all()

            table = jobsTable(job_list)
            table.order_by = "-jobAnnounceDate"
            RequestConfig(request, paginate={"per_page": 20}).configure(table)

            context['table'] = table
            context["jobs"] = job_list
            context["tt"] = '職缺標題'

            from .export import TableExport

            export_format = request.GET.get('_export', None)

            if TableExport.is_valid_format(export_format):
                from .tables import jobsTable2
                tablee = jobsTable2(job_list)
                table = tablee
                exporter = TableExport(export_format, table)
                return exporter.response('File_Name.{}'.format(export_format))

        if load_template == 'charts-morris.html':
            job_list = Jobs.objects.all()
            df = pd.DataFrame(list(job_list.values()))
            freq = Jieba_Cut(df)  # 斷詞模組
            freqTable = freq.pd2frequency('')
            # 堆疊長條圖 - 薪水與職缺
            stackPlot = im_bar_stack(freq.df)
            context['stackPlot'] = stackPlot

            # 未堆疊長條圖 - 人數與職缺
            no_stackPlot = im_bar_nostack(freq.df)
            context['no_stackPlot'] = no_stackPlot

            # 長條圖折線圖 - 職缺薪水平均
            barLinePlot = im_bar_line(freq.df)
            context['barLinePlot'] = barLinePlot

            # 混合圖表 = 職缺文字不均度
            Woe, Spec, Ent, cor = freq.getMixedBarLineData()
            mixedPlot = im_mixed_bar_line(Woe, Spec, Ent)
            context['mixedPlot'] = mixedPlot

            # 圓餅圖 - 類別
            cat_dict = {i: 0 for i in name}
            for c in df['jobType'].values:
                w = c.split('、')
                if w[0] == '':
                    continue
                for i in w:
                    cat_dict[i] += 1

            piePlot_type = im_pie(jobN,
                                  list(cat_dict.values()))
            context['piePlot_type'] = piePlot_type
            # 圓餅圖 - 地點
            city = ['台北市', '高雄市', '新北市', '台中市',
                    '桃園市', '新竹市', '新竹縣', '台南市', '其它縣市']
            city_dict = {i: 0 for i in city}
            for c in df['jobLocation'].values:
                if c == '':
                    continue
                else:
                    c = c[:3]
                    if c in city:
                        city_dict[c] += 1
                    else:
                        city_dict['其它縣市'] += 1

            piePlot_region = im_pie(
                list(city_dict.keys()), list(city_dict.values()))
            context['piePlot_region'] = piePlot_region

            data = []
            for i in freqTable.values:
                if i[1] < 10:
                    continue
                data.append(tuple(i))

            wordCloud = im_word(data[:700])
            context['plot_div'] = wordCloud

            # BarPlot
            bar = freq.getBarData('')
            barPlot = im_bar(bar)

            context['bar'] = barPlot

        if load_template in industry:
            filter = name[industry.index(load_template)]
            job_list = Jobs.objects.all()
            df = pd.DataFrame(list(job_list.values()))
            freq = Jieba_Cut(df)  # 斷詞模組
            freqTable = freq.pd2frequency(filter)

            data = []
            for i in freqTable.values:
                if i[1] < 10:
                    continue
                data.append(tuple(i))

            wordCloud = im_word(data[:700])
            context['plot_div'] = wordCloud
            # BarPlot
            bar = freq.getBarData(filter)
            barPlot = im_bar(bar)

            context['bar'] = barPlot

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
