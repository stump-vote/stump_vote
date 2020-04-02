from django.contrib import admin
from .models import Sample

# Register your models here.


class SampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


admin.site.register(Sample, SampleAdmin)
