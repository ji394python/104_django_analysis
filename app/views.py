# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .scrappers import Klook
from .models import *
import pandas as pd
import os


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
            klook = Klook('test')
            print('有無元件')
            print(klook)
            klook = klook.scrape()
            print(klook)
            # title, link, push, date, author = [], [], [], [], []
            # for row in klook:
            #     title.append(str(row['title']))
            #     link.append(str(row['link']))
            #     push.append(str(row['price']))
            #     date.append(str(row['booking_date']))
            #     author.append(str(row['star']))
            # # print(os.path.exists('ptt.csv'), os.listdir('.'))
            # df = pd.DataFrame(
            #     {'title': title, 'link': link, 'push': push, 'date': date, 'author': author})
            # 0516 Heroku除資料庫外imuutable
            # if not os.path.exists('ptt.csv'):
            #     df = pd.DataFrame(
            #         {'標題': title, '連結': link, '推噓數': push, '日期': date, '作者': author})
            #     df.to_csv('ptt.csv', encoding='utf-8-sig', index=False)
            # else:
            #     origin = pd.read_csv('ptt.csv', encoding='utf-8-sig')
            #     df = pd.DataFrame(
            #         {'標題': title, '連結': link, '推噓數': push, '日期': date, '作者': author})
            #     df = df.append(origin)
            #     df.to_csv('ptt.csv', encoding='utf-8-sig', index=False)

            # user_list = []
            # for i in df.iterrows():
            #     i = i[1]
            #     d = {'title': i['title'], 'link': i['link'], 'price': i['push'],
            #          'booking_date': i['date'], 'star': i['author']}
            #     user_list.append(d)

            # 0516: SQLite在heroku會有問題，故改用csv
            for i in klook:
                title = str(i['title'])
                link = str(i['link'])
                price = str(i['price'])
                booking_date = str(i['booking_date'])
                star = str(i['star'])
                UserInfo.objects.create(
                    title=title, line=link, price=price, booking_date=booking_date, star=star)
                print('成功新增資料')
            user_list = UserInfo.objects.all()
            # return render(request, 'index.html', {'data': user_list,'logout':'#'})
            # user_list = [{'title': '[心得] 關於永豐的軟體', 'link': 'https://www.ptt.cc//bbs/Stock/M.1652616237.A.7C7.html',
            #               'price': '27', 'booking_date': ' 5/15', 'star': 'akwin'}]
            context["tickets"] = user_list
            print([klook[2]])
            # print(user_list)
            context["tt"] = '測試'
        if load_template == 'charts-morris.html':
            from pyecharts.charts import WordCloud, Bar
            from pyecharts import options as opts
            data = [
                ("生活资源", "999"),
                ("供热管理", "888"),
                ("供气质量", "777"),
                ("生活用水管理", "688"),
                ("一次供水问题", "588"),
                ("交通运输", "516"),
                ("城市交通", "515"),
                ("环境保护", "483"),
                ("房地产管理", "462"),
                ("城乡建设", "449"),
                ("社会保障与福利", "429"),
                ("社会保障", "407"),
                ("供热发展", "254"),
                ("农村土地规划管理", "254"),
                ("生活噪音", "253"),
                ("供热单位影响", "253"),
                ("城市供电", "223"),
                ("房屋质量与安全", "223"),
                ("大气污染", "223"),
                ("房屋安全", "223"),
                ("燃气管理", "152"),
                ("教育管理", "152"),
                ("医疗纠纷", "152"),
                ("宏观经济", "152"),
                ("教育管理", "112"),
                ("社会保障", "112"),
                ("二次供水问题", "112"),
                ("城市公共设施", "92"),
                ("社会保障保险管理", "92"),
                ("低保管理", "92"),
                ("文娱市场管理", "72"),
                ("城市交通秩序管理", "72"),
                ("执法争议", "72"),
                ("商业烟尘污染", "72"),
                ("占道堆放", "71"),
                ("地上设施", "71"),
                ("群众健身", "41"),
                ("工业排放污染", "41"),
                ("市场收费", "41"),
                ("生产资金", "41"),
                ("生产噪声", "41"),
                ("农村低保", "41"),
                ("劳动争议", "41"),
                ("劳动合同争议", "41"),
                ("劳动报酬与福利", "41"),
                ("医疗事故", "21"),
                ("停供", "21"),
                ("基础教育", "21"),
                ("市场外溢", "11"),
                ("占道经营", "11"),
                ("树木管理", "11"),
                ("农村基础设施", "11"),
                ("一次供水问题", "11"),
            ]

            x = (
                WordCloud()
                .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=True),
                )
                .render_embed()
            )
            context['plot_div'] = x
            c = (
                Bar(init_opts=opts.InitOpts(width="300px",
                                            height="300px",
                                            page_title="造价四剑客")
                    )
                .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
                .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
                .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
                .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题")).render_embed()
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
