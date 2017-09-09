from django.contrib import admin
from .models import Record, Medic, Doctor, Profession, Specialization, Qualification, MedicEmail


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'synced', 'created_on')
    list_filter = ['created_on']
    search_fields = ['file']


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'profession')
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name']


class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'profession')
    list_filter = ['created_at']
    search_fields = ['profession']


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialization')
    list_filter = ['created_at']
    search_fields = ['specialization']


class QualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'qualification', 'university')
    list_filter = ['created_at']
    search_fields = ['qualification', 'university']

admin.site.register(Record, RecordAdmin)
admin.site.register(Medic)
admin.site.register(MedicEmail)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Qualification, QualificationAdmin)
