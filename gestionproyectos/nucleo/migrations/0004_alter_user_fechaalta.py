# Generated by Django 3.2 on 2022-02-01 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0003_auto_20220201_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fechaAlta',
            field=models.DateField(null=True),
        ),
    ]
