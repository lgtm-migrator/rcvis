# Generated by Django 3.0.8 on 2021-05-14 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0021_jsonconfig_showroundnumbersonsankey'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsonconfig',
            name='dataSourceURL',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
    ]
