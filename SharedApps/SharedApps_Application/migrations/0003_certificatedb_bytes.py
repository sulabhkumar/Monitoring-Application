# Generated by Django 2.1.7 on 2019-05-22 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SharedApps_Application', '0002_certificatedb_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatedb',
            name='bytes',
            field=models.BinaryField(blank=True, editable=True),
        ),
    ]
