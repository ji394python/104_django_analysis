import django_tables2 as tables
from .models import Jobs
from django_filters.views import FilterView


class jobsTable(tables.Table):
    jobTitles = tables.TemplateColumn(
        '<a href="{{record.jobDetailUrl}}">{{record.jobTitles|truncatechars:32}}</a>')
    jobCompanyName = tables.TemplateColumn(
        '<a href="{{record.jobCompanyUrl}}">{{record.jobCompanyName|truncatechars:8}}</a>')
    jobCompanyIndustry = tables.TemplateColumn(
        '<span>{{record.jobCompanyIndustry|truncatechars:8}}</span>')
    jobRqDepartment = tables.TemplateColumn(
        '<span>{{record.jobRqDepartment|truncatechars:8}}</span>')
    jobCategory = tables.TemplateColumn(
        '<span>{{record.jobCategory|truncatechars:12}}</span>')
    jobContent = tables.TemplateColumn(
        '<span>{{record.jobContent|truncatechars:20}}</span>')
    jobSpecialty = tables.TemplateColumn(
        '<span>{{record.jobContent|truncatechars:12}}</span>')
    jobOthers = tables.TemplateColumn(
        '<span>{{record.jobOthers|truncatechars:12}}</span>')
    jiebaCut = tables.TemplateColumn(
        '<span>{{record.jiebaCut|truncatechars:12}}</span>')

    class Meta:
        model = Jobs
        # add class="paleblue" to <table> tag
        exclude = ('id', "jobCompanyUrl",
                   "jobDetailUrl", 'jobType')  # 可以隱藏欄位
        # sequence = ("last_name", "first_name", "birth_date", )  # 可以調整順序

        template_name = "django_tables2/bootstrap4.html"
        attrs = {
            'class': 'table table-striped'
        }
        order_by_field = 'sort_by'  # default: sort


class jobsTable2(tables.Table):

    class Meta:
        model = Jobs
        # add class="paleblue" to <table> tag
        exclude = ('id', "jobCompanyUrl",
                   "jobDetailUrl", 'jobType')  # 可以隱藏欄位
        # sequence = ("last_name", "first_name", "birth_date", )  # 可以調整順序

        template_name = "django_tables2/bootstrap4.html"
        attrs = {
            'class': 'table table-striped'
        }
        order_by_field = 'sort_by'  # default: sort
