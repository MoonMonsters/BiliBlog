# Generated by Django 2.0.2 on 2018-06-18 14:27

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0010_auto_20180618_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=DjangoUeditor.models.UEditorField(verbose_name='博客内容'),
        ),
    ]