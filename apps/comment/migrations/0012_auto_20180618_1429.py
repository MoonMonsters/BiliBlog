# Generated by Django 2.0.2 on 2018-06-18 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0011_auto_20180618_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
    ]
