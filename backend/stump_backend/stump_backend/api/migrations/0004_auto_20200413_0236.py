# Generated by Django 3.0.4 on 2020-04-13 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200413_0157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsfeeddemoitem',
            options={'ordering': ['-pub_date']},
        ),
    ]
