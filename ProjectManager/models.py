from django.db import models
from django.contrib.auth.models import User

# to query a user's projects
# <user>.project_set.all()

# import datetime
# d = datetime.date(1997, 10, 19)

# Project
    # title, desc, number tasks, deadline, progress
class Project(models.Model):
    project_owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=50) #, unique=True)
    project_description = models.TextField(blank=True, null=True)
    number_of_tasks = models.IntegerField(default=0)
    project_deadline = models.DateField(blank=True, null=True)
    project_progress = models.FloatField(default=0)

    # function that auto-updates and sets the project progress
    # function that auto-updates number_of_tasks

    def __str__(self):
        return self.project_title

# Groups (tasks are grouped [overlap?])
    #group_name
class Group_Type(models.Model):
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_type

# Person (assigned to tasks)
    # first, last, email
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True, null=True)

    # func to notify when someone has been added to a project

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Task
    # title, desc, project, groups, people assigned, date created, deadline (opt)
class Task(models.Model):
    task_title = models.CharField(max_length=100)
    task_description = models.TextField()
    task_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # make these next two fields optional? ***
    task_groups = models.ManyToManyField(Group_Type, help_text="What group does this task belong to?", blank=True)
    people_assigned = models.ManyToManyField(Person, help_text="Who is working on this task?", blank=True)
    task_complete = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True, editable=False)
    deadline = models.DateField(blank=True, null=True)

    # if datetime > deadline, return BEHIND SCHEDULE
    # if now > deadline / 2, return APPROACHNG DEADLINE
    # else return ON SCHEDULE

    def __str__(self):
        return f'{self.task_title} - {self.task_description}'

# Note
    # text, project, task (opt)
class Note(models.Model):
    note_text = models.TextField()
    project = models.ForeignKey(Task, on_delete=models.CASCADE)
    task = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
