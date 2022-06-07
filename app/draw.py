from pyecharts.charts import WordCloud, Bar, Pie, Page, Line
from pyecharts import options as opts
from pyecharts.globals import SymbolType, ThemeType
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.commons.utils import JsCode
import re


def im_word(data):
    '''
        Word Cloud
    '''
    embed = (
        WordCloud(init_opts=opts.InitOpts(
            width='100%', height='600px'))
        .add(series_name="文字雲", data_pair=data[:250], word_size_range=[15, 60], shape='diamond')
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
            toolbox_opts=opts.ToolboxOpts(is_show=False)

        )
        .render_embed()
    )
    return embed


def im_bar(data):
    '''
        bar plot
    '''
    embed = (
        Bar(init_opts=opts.InitOpts(width="100%",
                                    height="500px",
                                    page_title="柱狀圖")
            )
        .add_xaxis(data[0])
        .add_yaxis("Top30 雙詞彙組", data[1], itemstyle_opts=opts.ItemStyleOpts(color='#2177B4'))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="", subtitle="齊夫法則"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color='black', font_size=12))
        ).render_embed()
    )
    return embed


def im_pie(category: list, data: list):
    embed = (
        Pie(init_opts=opts.InitOpts(width="100%",
                                    height="700px",
                                    page_title="圓餅圖")
            )
        .add(
            "",
            [list(z) for z in zip(category, data)],
            radius=["50%", "70%"],
            label_opts=opts.LabelOpts(is_show=True, position="outside"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="15%", pos_top='5%', orient="horizontal"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"), tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),)
        .render_embed()
    )
    return embed


def im_bar_stack(df):
    name = ["資訊工程", "數據分析", "行銷企劃", "行政助理", "藝術設計", "餐飲", "服務", "技術與操作", "教育"]
    sal = ['月薪', '時薪', '待遇面議', '論件計酬', '其它']
    salary = {i: {k: 0 for k in name} for i in sal}

    for ro in df[['jobSalary', 'jobType']].iterrows():
        ro = ro[1]
        for n in name:
            if isinstance(ro['jobType'], float) and np.isnan(ro['jobType']):
                break
            if n in ro['jobType']:
                check = True
                for sa in salary.keys():
                    if isinstance(ro['jobSalary'], float) and np.isnan(ro['jobSalary']):
                        break
                    if sa in ro['jobSalary']:
                        salary[sa][n] += 1
                        check = False
                if check:
                    salary['其它'][n] += 1

    conduct = {i: [] for i in sal}
    rows = [[i] for i in sal]
    for k in name:
        total = 0
        for n in sal:
            total += salary[n][k]
        for n in sal:
            conduct[n].append(
                {'value': round(salary[n][k]/total, 2), 'percent': round(salary[n][k]/total, 4)})
            rows[sal.index(n)].append(f"{round(salary[n][k]/total*100,2)}%")

    headers = ["", "資訊工程", "數據分析", "行銷企劃", "行政助理",
               "媒體設計", "餐飲飯店", "服務業", "技術員", "教育補教"]

    table = Table()
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="", subtitle="")
    )

    c = (
        Bar(init_opts=opts.InitOpts(
            theme=ThemeType.LIGHT, width="100%", height="600px"))
        .add_xaxis(["資訊工程", "數據分析", "行銷企劃", "行政助理", "媒體設計", "餐飲飯店", "服務業", "技術員", "教育補教"])
        .add_yaxis("月薪", conduct['月薪'], stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color='#C0504D'))
        .add_yaxis("時薪", conduct['時薪'], stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color='#4F81BD'))
        .add_yaxis("待遇面議", conduct['待遇面議'], stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color='#8064A2'))
        .add_yaxis("論件計酬", conduct['論件計酬'], stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color='#9BBB59'))
        .add_yaxis("其它", conduct['其它'], stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color='#4BACC6'))
        .set_series_opts(
            label_opts=opts.LabelOpts(
                is_show=False,
                position="center",
                color="black",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                type_="value",
                min_=0,
                max_=1,
                interval=0.1,
                axislabel_opts=opts.LabelOpts(formatter=JsCode(
                    "function(x){return Number(x * 100).toFixed() + '%';}"
                )),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
    )

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        c,
        table
    )

    return page.render_embed()


def im_mixed_bar_line(Woe, Spec, Ent):
    head = ["資訊工程", "數據分析", "行銷企劃", "行政助理",
            "媒體設計", "餐飲飯店", "服務業", "技術員", "教育補教"]
    colors = ['#5793f3', '#d14a61', '#d14a61']
    bar = (
        Bar(init_opts=opts.InitOpts(width="100%", height="600px"))
        .add_xaxis(xaxis_data=head)
        .add_yaxis(
            series_name="詞彙數",
            y_axis=Spec,
            yaxis_index=0,
            color=colors[1],
        )
        .add_yaxis(
            series_name="平均字數", y_axis=Woe, yaxis_index=1, color=colors[0]
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="平均字數",
                type_="value",
                min_=0,
                max_=1000,
                interval=100,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=colors[1])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="Entropy",
                min_=9,
                max_=11,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#000')
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="詞彙數",
                min_=0,
                max_=12000,
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=colors[0])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis", axis_pointer_type="cross"),
        )
    )
    line = (
        Line()
        .add_xaxis(xaxis_data=head)
        .add_yaxis(
            series_name="Entropy", y_axis=Ent, yaxis_index=2
        )
        .set_series_opts(
            linestyle_opts=opts.LineStyleOpts(color=colors[2], width=2)
        )
    )

    bar = bar.overlap(line)

    headers = ["", "資訊工程", "數據分析", "行銷企劃", "行政助理",
               "媒體設計", "餐飲飯店", "服務業", "技術員", "教育補教"]
    table = Table()
    rows = [['平均字數'], ['總詞彙數'], ['Entropy']]
    rows[0].extend(Woe)
    rows[1].extend(Spec)
    rows[2].extend(Ent)

    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="", subtitle="")
    )

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        bar,
        table
    )
    return page.render_embed()


def im_bar_nostack(df):

    apply = ['0~5人', '6~10人', '11~30人', '大於30人']
    name = ["資訊工程", "數據分析", "行銷企劃", "行政助理", "藝術設計", "餐飲", "服務", "技術與操作", "教育"]
    Apply = {i: {k: 0 for k in name} for i in apply}

    for ro in df[['jobApplyNums', 'jobType']].iterrows():
        ro = ro[1]
        for n in name:
            if isinstance(ro['jobType'], float) and np.isnan(ro['jobType']):
                break
            if n in ro['jobType']:
                for sa in Apply.keys():
                    if isinstance(ro['jobApplyNums'], float) and np.isnan(ro['jobApplyNums']):
                        break
                    if sa in ro['jobApplyNums']:
                        Apply[sa][n] += 1

    rows = [[i] for i in apply]
    rows2 = [[i] for i in apply]
    for k in name:
        total = 0
        for n in apply:
            total += Apply[n][k]
        for n in apply:
            rows[apply.index(n)].append(round(Apply[n][k]/total, 4))
            rows2[apply.index(n)].append(f"{round(Apply[n][k]/total*100,2)}%")

    headers = ["", "資訊工程", "數據分析", "行銷企劃", "行政助理",
               "媒體設計", "餐飲飯店", "服務業", "技術員", "教育補教"]

    table = Table()
    table.add(headers, rows2)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="", subtitle="")
    )

    c = (
        Bar({"theme": ThemeType.LIGHT})
        .add_xaxis(name)
        .add_yaxis("0~5人", [i for i in rows[0][1:]])
        .add_yaxis("6~10人", [i for i in rows[1][1:]])
        .add_yaxis("11~30人", [i for i in rows[2][1:]])
        .add_yaxis("大於30人", [i for i in rows[3][1:]])
        .set_global_opts(
            title_opts={"職缺應徵人數柱狀圖"}
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                is_show=False
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                type_="value",
                min_=0,
                max_=0.9,
                interval=0.1,
                axislabel_opts=opts.LabelOpts(formatter=JsCode(
                    "function(x){return Number(x * 100).toFixed() + '%';}"
                )),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
    )

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        c,
        table
    )

    return page.render_embed()


def im_bar_line(df):

    name = ["資訊工程", "數據分析", "行銷企劃", "行政助理", "藝術設計", "餐飲", "服務", "技術與操作", "教育"]
    sal = ['月薪', '時薪']
    salary = {i: {k: [] for k in name} for i in sal}

    for ro in df[['jobSalary', 'jobType']].iterrows():
        ro = ro[1]
        for n in name:
            if isinstance(ro['jobType'], float) and np.isnan(ro['jobType']):
                break
            if n in ro['jobType']:
                for sa in salary.keys():
                    if isinstance(ro['jobSalary'], float) and np.isnan(ro['jobSalary']):
                        break
                    if sa in ro['jobSalary']:
                        salar = re.findall('[0-9,]+', ro['jobSalary'])
                        if len(salar) == 0:
                            continue
                        elif len(salar) == 1:
                            salary[sa][n].append(
                                int(salar[0].replace(',', '')))
                        elif len(salar) == 2:
                            salar = (int(salar[0].replace(
                                ',', '')) + int(salar[1].replace(',', ''))) / 2
                            salary[sa][n].append(salar)
                        else:
                            print(ro['jobSalary'])

    for k, v in salary.items():
        for k2, v2 in v.items():
            salary[k][k2] = round(sum(v2)/len(v2), 2)

    bar = (
        Bar({"theme": ThemeType.LIGHT, 'init_opts': opts.InitOpts(
            width="100%", height="800px")})
        .add_xaxis(xaxis_data=name)
        .add_yaxis(
            series_name="平均月薪",
            y_axis=list(salary['月薪'].values()),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="平均時薪",
                type_="value",
                min_=100,
                max_=210,
                interval=10,
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, type_="shadow"),
            ),
            yaxis_opts=opts.AxisOpts(
                name="平均月薪",
                type_="value",
                min_=20000,
                max_=40000,
                interval=2000,
                axislabel_opts=opts.LabelOpts(formatter="{value} "),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
    )

    line = (
        Line()
        .add_xaxis(xaxis_data=name)
        .add_yaxis(
            series_name="平均時薪",
            yaxis_index=1,
            y_axis=list(salary['時薪'].values()),
            label_opts=opts.LabelOpts(is_show=False),
        )
    ).set_series_opts(
        linestyle_opts=opts.LineStyleOpts(width=2)
    )

    plot = bar.overlap(line)

    rows = [[i] for i in sal]
    rows[0].extend(list(salary[rows[0][0]].values()))
    rows[1].extend(list(salary[rows[1][0]].values()))

    headers = ["", "資訊工程", "數據分析", "行銷企劃", "行政助理",
               "媒體設計", "餐飲飯店", "服務業", "技術員", "教育補教"]
    table = Table()
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="", subtitle="")
    )

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        plot,
        table
    )
    print(page)
    return page.render_embed()
