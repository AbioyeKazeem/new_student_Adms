# Generated by Django 5.1.3 on 2024-12-09 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_adms', '0008_alter_courseregistration_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseregistration',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='courseregistration',
            name='admitted_candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_adms.admittedcandidate'),
        ),
        migrations.AlterField(
            model_name='courseregistration',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_adms.course'),
        ),
        migrations.AlterField(
            model_name='courseregistration',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='courseregistration',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
