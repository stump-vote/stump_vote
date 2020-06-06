from django.contrib import admin
from .models import Sample, NewsfeedDemoItemType, NewsfeedDemoTopic, NewsfeedDemoItem, NewsfeedDemoBill

# Register your models here.


class SampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class NewsfeedDemoItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


class NewsfeedDemoTopicAdmin(admin.ModelAdmin):
    list_display = ('name', )


class NewsfeedDemoBillAdmin(admin.ModelAdmin):
    list_display = ('name', )


class NewsfeedDemoItemAdmin(admin.ModelAdmin):
    list_display = ('feed_key', 'item_type', 'topic')


admin.site.register(Sample, SampleAdmin)
admin.site.register(NewsfeedDemoItemType, NewsfeedDemoItemTypeAdmin)
admin.site.register(NewsfeedDemoTopic, NewsfeedDemoTopicAdmin)
admin.site.register(NewsfeedDemoBill, NewsfeedDemoBillAdmin)
admin.site.register(NewsfeedDemoItem, NewsfeedDemoItemAdmin)
