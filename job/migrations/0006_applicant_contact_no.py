# Generated by Django 3.2.9 on 2022-01-18 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_applyjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='contact_no',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
