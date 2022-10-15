# Generated by Django 4.1.1 on 2022-10-15 14:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=64)),
                ("nickName", models.CharField(max_length=8)),
                ("totalSpending", models.FloatField()),
                ("balance", models.FloatField()),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=16)),
                ("createDate", models.DateTimeField(default=django.utils.timezone.now)),
                ("updateDate", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="OperationsHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("operationType", models.CharField(max_length=8)),
                (
                    "operateTime",
                    models.DateTimeField(verbose_name=django.utils.timezone.now),
                ),
                ("oid", models.IntegerField()),
                ("vid", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Operators",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=8)),
                ("repairedVehicles", models.IntegerField()),
                ("chargedVehicles", models.IntegerField()),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=16)),
                ("createDate", models.DateTimeField(default=django.utils.timezone.now)),
                ("updateDate", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Payments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                ("status", models.CharField(default="success", max_length=8)),
                (
                    "payTime",
                    models.DateTimeField(verbose_name=django.utils.timezone.now),
                ),
                ("cid", models.IntegerField()),
                ("vid", models.IntegerField()),
                ("detail", models.CharField(default="", max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="RepairHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("repairedLoc", models.CharField(max_length=16)),
                (
                    "repairedTime",
                    models.DateTimeField(verbose_name=django.utils.timezone.now),
                ),
                ("oid", models.IntegerField()),
                ("vid", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="TopUpHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.IntegerField()),
                ("status", models.CharField(max_length=8)),
                (
                    "topTime",
                    models.DateTimeField(verbose_name=django.utils.timezone.now),
                ),
                ("cid", models.IntegerField()),
                ("detail", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Vehicles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=8)),
                ("cover", models.ImageField(upload_to="covers")),
                ("color", models.CharField(max_length=8)),
                ("plateNum", models.IntegerField()),
                ("batteryPercentage", models.IntegerField()),
                ("lastChargedTime", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(max_length=32)),
                ("totalRentalHours", models.FloatField()),
                ("locName", models.CharField(max_length=16)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
        ),
    ]
