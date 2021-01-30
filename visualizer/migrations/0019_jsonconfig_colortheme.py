# Generated by Django 3.0.8 on 2021-01-29 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0018_jsonconfig_dousedescriptioninsteadoftimeline'),
    ]

    operations = [migrations.AddField(model_name='jsonconfig', name='colorTheme', field=models.IntegerField(
        choices=[(0, 'Full color spectrum'), (1, 'Purple to orange'), (2, 'Alternating colors')], default=0), ), ]
