from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_content', 'created_at', 'updated_at', 'doctor')
    list_filter = ['created_at', 'updated_at',]
    search_fields = ['id', 'doctor']


admin.site.register(Post, PostAdmin)
# admin.site.register(Medic)
# admin.site.register(Doctor)