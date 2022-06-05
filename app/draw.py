from pyecharts.charts import WordCloud, Bar, Pie
from pyecharts import options as opts
from pyecharts.globals import SymbolType


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
