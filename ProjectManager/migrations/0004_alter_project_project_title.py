# Generated by Django 4.0.4 on 2022-08-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectManager', '0003_alter_project_project_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_title',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]