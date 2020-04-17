from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.


class Sample(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.title


class NewsfeedDemoItemType(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return self.name


class NewsfeedDemoTopic(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return self.name


class NewsfeedDemoBill(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return self.name


class NewsfeedDemoItem(models.Model):
    item_type = models.ForeignKey(NewsfeedDemoItemType, on_delete=models.PROTECT)
    topic = models.ForeignKey(NewsfeedDemoTopic, on_delete=models.PROTECT)
    pub_date = models.DateTimeField()
    feed_key = models.CharField(max_length=32)
    content = JSONField(default=dict)
    main_image = models.URLField(null=True, blank=True)
    bill = models.ForeignKey(NewsfeedDemoBill, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['-pub_date']
