# Generated by Django 4.1.2 on 2022-10-17 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_portal', '0003_remove_operators_chargedvehicles_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customers',
            old_name='nickName',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='customers',
            name='address',
            field=models.CharField(default='', max_length=64),
        ),
    ]
