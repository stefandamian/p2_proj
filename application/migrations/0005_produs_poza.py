# Generated by Django 3.1.7 on 2021-05-07 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_lista_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='produs',
            name='poza',
            field=models.URLField(max_length=450, null=True),
        ),
    ]
