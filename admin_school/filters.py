import django_filters
from manager_school.models import Costs


class CostsFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFromToRangeFilter(
    label = 'Введите дату в диапазоне от и до',
    widget = django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd'}))

    class Meta:
        model = Costs
        fields = ['date']