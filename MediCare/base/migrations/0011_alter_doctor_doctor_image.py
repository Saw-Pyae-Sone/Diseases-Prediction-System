# Generated by Django 4.2.7 on 2024-03-21 13:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0010_rename_doctor_langauges_doctor_doctor_languages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="Doctor_Image",
            field=models.ImageField(
                blank=True, null=True, upload_to="customadmin/static/cimg/"
            ),
        ),
    ]