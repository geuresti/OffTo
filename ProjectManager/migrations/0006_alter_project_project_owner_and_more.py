# Generated by Django 4.0.4 on 2022-08-25 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ProjectManager', '0005_alter_task_people_assigned_alter_task_task_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='people_assigned',
            field=models.ManyToManyField(blank=True, help_text='Who is working on this task?', to='ProjectManager.person'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_groups',
            field=models.ManyToManyField(blank=True, help_text='What group does this task belong to?', to='ProjectManager.group_type'),
        ),
    ]
