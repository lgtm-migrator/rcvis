# Generated by Django 3.0.8 on 2021-05-15 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0021_jsonconfig_showroundnumbersonsankey'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsonconfig',
            name='areResultsCertified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jsonconfig',
            name='candidateSidecarFile',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='jsonconfig',
            name='dataSourceURL',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
    ]
