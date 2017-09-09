from django.contrib import admin
from .models import Country, City, Event, EventTopic, EventType, Scholarship, ScholarshipCategory, Job, JobCategory


# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'continent')
    list_filter = ['name']
    search_fields = ['name']


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_filter = ['name']
    search_fields = ['name']


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_on')
    list_filter = ['title']
    search_fields = ['title']


class EventTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ['name']
    search_fields = ['name']


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ['name']
    search_fields = ['name']


class ScholarshipCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ['name']
    search_fields = ['name']


class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ['title']
    search_fields = ['title']


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ['name']
    search_fields = ['name']


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ['title']
    search_fields = ['title']


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventTopic, EventTopicAdmin)
admin.site.register(Scholarship, ScholarshipAdmin)
admin.site.register(ScholarshipCategory, ScholarshipCategoryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)