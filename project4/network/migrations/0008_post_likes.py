# Generated by Django 4.2.4 on 2023-10-18 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_post_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default='0'),
        ),
    ]