from .models import ClassModel, StudyRequest, CourseUser, AdvUser
from rest_framework import serializers


class ClassModelSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return f"{obj.date.strftime('%d.%m.%Y')} {obj.start_time.strftime('%H:%M')}-{obj.end_time.strftime('%H:%M')}"

    class Meta:
        model = ClassModel
        fields = ['id', 'date', 'theme', 'position']


class StudyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyRequest
        fields = ['id', 'first_name', 'enter_date', 'email', 'tel_number', 'course']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseUser
        fields = ('id', 'title', 'price', 'start_date', 'finish_date', 'img', 'amount', 'is_online')


class CourseTeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvUser
        fields = ('id', 'first_name', 'last_name', 'surname', 'img_user')


class CourseDetailSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()

    def get_teachers(self, obj):
        print(obj)
        teachers = AdvUser.objects.filter(groups__name="Teacher", groups_teacher__in=obj.groups.all())
        return CourseTeachersSerializer(set(teachers), many=True).data

    class Meta:
        model = CourseUser
        fields = ('id', 'title', 'description', 'price', 'start_date', 'finish_date', 'img', 'amount', 'is_online', 'teachers')