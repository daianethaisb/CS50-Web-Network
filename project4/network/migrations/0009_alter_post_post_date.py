# Generated by Django 4.2.4 on 2023-10-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(null=True),
        ),
    ]