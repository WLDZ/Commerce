# Generated by Django 3.2.3 on 2021-06-12 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210613_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='url',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
