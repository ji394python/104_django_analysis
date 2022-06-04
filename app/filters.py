from .models import Jobs
import django_filters


class JobFilter(django_filters.FilterSet):

    class Meta:
        model = Jobs
        fields = ['jobAnnounceDate']  # 選擇用哪欄篩選
