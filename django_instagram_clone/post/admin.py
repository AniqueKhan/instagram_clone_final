from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user','caption']

admin.site.register(models.Tag)
admin.site.register(models.Follow)
admin.site.register(models.Stream)
admin.site.register(models.PostFileContent)
