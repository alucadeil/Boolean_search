# Generated by Django 3.1.1 on 2020-10-01 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_document_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='url',
            field=models.CharField(default='Sample text', max_length=1000, null=True),
        ),
    ]
