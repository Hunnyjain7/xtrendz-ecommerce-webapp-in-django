# Generated by Django 3.2.9 on 2021-12-12 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_edition_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]