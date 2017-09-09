from django.contrib import admin
from .models import MedicalCase, MedicalCaseCategory, Comment, Reply, Photo


class MedicalCaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'chief_complaint', 'patient_age', 'patient_gender', 'patient_country_of_origin',
                    'history_of_present_illness', 'medical_history', 'surgical_history', 'social_history',
                    'family_history','allergies', 'medications', 'review_of_systems', 'physical_examination',
                    'diagnostic_tests', 'medical_case_categories', 'created_at', 'updated_at', 'doctor']
    list_filter = ['created_at', 'updated_at', ]
    search_fields = ['id', 'doctor']

    def medical_case_categories(self, obj):
        return ",".join([medical_case_category.name for medical_case_category in obj.MedicalCaseCategory.all()])


admin.site.register(MedicalCase, MedicalCaseAdmin)
admin.site.register(MedicalCaseCategory)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Photo)
