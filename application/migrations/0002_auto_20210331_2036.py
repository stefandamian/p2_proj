# Generated by Django 3.1.7 on 2021-03-31 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produs',
            name='url',
            field=models.URLField(max_length=450),
        ),
    ]
