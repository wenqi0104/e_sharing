# Generated by Django 4.1.1 on 2022-10-30 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("e_portal", "0008_alter_order_endtime_alter_order_starttime"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicles",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="vehicles",
            name="name",
            field=models.CharField(default="car", max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order", name="endTime", field=models.DateTimeField(default=""),
        ),
    ]
