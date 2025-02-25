# Generated by Django 5.1.6 on 2025-02-18 02:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('github', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(choices=[('PhD', 'Doctorate'), ('MTech/MA/MSc/MCom/MBA', 'Masters'), ('BE/BTech/BA/BSc/BCom', 'Bachelors'), ('12th', 'High School')], max_length=50)),
                ('stream', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=255)),
                ('start_year', models.DateField()),
                ('passing_year', models.DateField()),
                ('result', models.CharField(max_length=10)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fyf_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='AreaOfInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_of_interest_detail', models.TextField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fyf_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='Academics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_detail', models.TextField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fyf_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionalSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100)),
                ('proficiency_level', models.CharField(max_length=50)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fyf_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOrJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work', models.CharField(choices=[('J', 'Job'), ('P', 'Project')], max_length=1)),
                ('title', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField()),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('github_link', models.URLField(blank=True, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fyf_app.person')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fyf_app.person')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('academics', models.ManyToManyField(to='fyf_app.academics')),
                ('education', models.ManyToManyField(to='fyf_app.education')),
                ('interests', models.ManyToManyField(to='fyf_app.areaofinterest')),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fyf_app.person')),
                ('skills', models.ManyToManyField(to='fyf_app.professionalskills')),
                ('work_experience', models.ManyToManyField(to='fyf_app.projectorjob')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fyf_app.userprofile')),
            ],
        ),
    ]
