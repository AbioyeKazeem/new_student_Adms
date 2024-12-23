# Generated by Django 5.1.3 on 2024-12-04 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_adms', '0002_alter_admissionform_academic_transcripts_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_name', models.CharField(max_length=255)),
                ('candidate_email', models.EmailField(max_length=254)),
                ('submitted_answers', models.JSONField()),
                ('score', models.FloatField(blank=True, null=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CBTQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('options', models.JSONField()),
                ('correct_answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='admissionform',
            name='academic_transcripts',
            field=models.FileField(blank=True, null=True, upload_to='documents/academic_transcripts/'),
        ),
        migrations.AlterField(
            model_name='admissionform',
            name='birth_certificate',
            field=models.FileField(blank=True, null=True, upload_to='documents/birth_certificates/'),
        ),
        migrations.AlterField(
            model_name='admissionform',
            name='medical_fitness_report',
            field=models.FileField(blank=True, null=True, upload_to='documents/medical_reports/'),
        ),
    ]
