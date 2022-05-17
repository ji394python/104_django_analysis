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
