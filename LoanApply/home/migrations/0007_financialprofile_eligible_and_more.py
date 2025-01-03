# Generated by Django 5.1.4 on 2025-01-03 10:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_bankdata_cibildata'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='financialprofile',
            name='eligible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='financialprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
