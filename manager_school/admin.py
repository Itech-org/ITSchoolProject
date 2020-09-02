from django import forms
from django.contrib import admin
from .models import *
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
# Register your models here.

@admin.register(AdvUser)
class AdminViewAdvUser(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'phone',)
    search_fields = ('groups', )
    list_filter = ('groups',)


@admin.register(CourseUser)
class AdminViewCourseUser(admin.ModelAdmin):
    list_display = ('title', 'price', 'start_date', 'finish_date', 'is_online')
    prepopulated_fields = {'slug': ('title',)}


class ClassInline(admin.StackedInline):
    model = ClassModel
    extra = 0
    prepopulated_fields = {'slug': ('theme',)}


@admin.register(GroupModel)
class AdminViewGroupModel(admin.ModelAdmin):
    list_display = ('title', 'course')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['course']
    # inlines = [ClassInline]


class AttendanceInline(admin.StackedInline):
    model = Attendance
    extra = 0


@admin.register(ClassModel)
class AdminViewClassModel(admin.ModelAdmin):
    list_display = ('theme', 'date',)
    exclude = ('slug',)
    # prepopulated_fields = {'slug': ('theme',)}
    list_filter = ['groups']
    inlines = [AttendanceInline]


@admin.register(Classroom)
class AdminViewClassroom(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(HomeworkModel)
class AdminViewHomeworkModel(admin.ModelAdmin):
    list_display = ('title', )
    # prepopulated_fields = {'slug': ('title',)}

@admin.register(HomeworkTeacherModel)
class AdminViewHomeworkTeacherModel(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title',)}

@admin.register(MaterialText)
class AdminViewMaterialsText(admin.ModelAdmin):
    list_display = ('title', 'description', )
    prepopulated_fields = {'slug': ('title',)}

@admin.register(MaterialVideo)
class AdminViewMaterialsVideo(admin.ModelAdmin):
    list_display = ('title', 'description', )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'created' )
    prepopulated_fields = {'slug': ('title',)}

class RequestConversationInline(admin.StackedInline):
    model = RequestConversation
    extra = 0


@admin.register(StudyRequest)
class StudyRequestAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'enter_date', 'status')
    search_fields = ('status', 'enter_date', 'last_name', 'first_name',
                     'course__title', 'specialist__first_name', 'specialist__last_name',)
    fields = ('last_name', 'first_name', 'patronymic', 'enter_date', 'communication_type',
              'source', 'course',  'specialist', 'status')
    list_filter = ['enter_date', 'course', 'status']
    inlines = [RequestConversationInline]
    def formfield_for_foreignkey( self,  db_field,  request,  ** kwargs):
        if db_field.name ==  "specialist":
            kwargs["queryset"]  =  AdvUser.objects.filter(groups__name="Manager")
        return super().formfield_for_foreignkey( db_field,  request,  **kwargs)


class PaymentStageInline(NestedStackedInline):
    model = PaymentStage
    extra = 0
    fk_name = 'payment'


class UserPaymentInline(NestedStackedInline):
    model = UserPayment
    extra = 0
    fk_name = 'contract'
    inlines = [
        PaymentStageInline,
    ]


@admin.register(Contract)
class AdminViewClassModel(NestedModelAdmin):
    list_display = ('number', 'date', 'course')
    list_filter = ['date', 'course', 'group']
    inlines = [UserPaymentInline,]


@admin.register(PaymentStage)
class PaymentStageAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'price', 'date')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message',)

@admin.register(Costs)
class AdminCosts(admin.ModelAdmin):

    date_hierarchy = 'date'
    list_display = ('date', 'breakdown', 'chancery', 'grocery', 'house_chemicals','total')
    list_filter = ['date', 'total']


admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(UserManagement)
admin.site.register(RubruckNews)
admin.site.register(ContactAdmin)
admin.site.register(PersonalNotification)

