# Generated by Django 4.2.7 on 2024-02-08 12:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_topic_room_host_massage_room_topic"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                ("Patient_ID", models.IntegerField(primary_key=True, serialize=False)),
                ("Patient_Name", models.CharField(max_length=200)),
                ("Patient_Email", models.CharField(max_length=255)),
                ("Patient_Password", models.CharField(max_length=255)),
                ("Patient_Address", models.CharField(max_length=255)),
                (
                    "Patient_Family_Medical_History",
                    models.ImageField(upload_to="static/Image"),
                ),
            ],
        ),
    ]
