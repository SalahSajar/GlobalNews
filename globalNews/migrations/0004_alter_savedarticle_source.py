# Generated by Django 4.1.3 on 2023-02-12 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalNews', '0003_remove_savedarticle_article_savers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedarticle',
            name='source',
            field=models.CharField(default='', max_length=20),
        ),
    ]
