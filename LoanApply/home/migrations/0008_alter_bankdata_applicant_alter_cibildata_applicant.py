# Generated by Django 5.1.4 on 2025-01-03 10:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_financialprofile_eligible_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdata',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cibildata',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cibil_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
