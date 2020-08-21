from manager_school.models import ClassModel
from rest_framework import serializers


class ClassModelSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return f"{obj.date.strftime('%d.%m.%Y')} {obj.start_time.strftime('%H:%M')}-{obj.end_time.strftime('%H:%M')}"

    class Meta:
        model = ClassModel
        fields = ['id', 'date', 'theme', 'position']
