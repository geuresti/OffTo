from django.forms import ModelForm, Textarea
from django import forms
from django.core.exceptions import ValidationError
from .models import Project, Group_Type, Note, Task, Person

# can turn a model into a form using forms.ModelForm
# this requires setting the Meta class so the form
# knows what model / fields to use

# 'intial=...' for default form values upon rendering an unbound form
# 'widget=...' allows widget specification for when form is rendered
#       each field type has a default widget
# error messages, validators, ...
# fields: bool, char, choice, date/dtime, file, filepath,
#           decimal, duration, email, float, ip, image,
#           int, json, multi-choice, slug, ...
# To render a form in a template: {{ form }} (.as_table, .as_p, .as_ul)
#       or it can be done MANUALLY (might give more flexibility in design)

class LogInForm(forms.Form):
    username = forms.CharField(label="Username:")
    password = forms.CharField(label="Password:", widget=forms.PasswordInput)

class CreateAccountForm(forms.Form):
    email = forms.EmailField(required=False, help_text="(optional)")
    username = forms.CharField(label="Username:")
    password = forms.CharField(label="Password:", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm Password:",
        widget=forms.PasswordInput
    )

    # form validation
    def clean(self):
        clean_data = self.cleaned_data
        password = clean_data.get("password")
        confirm_password = clean_data.get("confirm_password")

        if password != confirm_password:
            # no visible notification, page simply refreshes
            # maybe send a context upon form.is_valid = False
            raise ValidationError("Your password was retyped incorrectly.")

        return clean_data

# number_of_tasks / project_progress should not be on the form
# project_deadline should be optional
class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['project_title', 'project_description', 'project_deadline']
        widgets = {
            'project_title': forms.TextInput(attrs={'placeholder':"Project Title"}),
            'project_description': forms.Textarea(attrs={'placeholder':"Project Description"}),
            'project_deadline': forms.DateInput(attrs={'type':'date'})
        }

"""
    group_name = models.CharField(max_length=50)
"""
class GroupTypeForm(ModelForm):

    class Meta:
        model = Group_Type
        fields = ['group_name']

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = [
            'task_title', 'task_description', 'task_complete', 'deadline'
        ]
        widgets = {
            'task_title': forms.TextInput(attrs={'placeholder':"Task Title"}),
            'task_description': forms.Textarea(attrs={'placeholder':"Task Description"}),
            'task_complete': forms.CheckboxInput(),
            'deadline': forms.DateInput(attrs={'type':'date'})
        }
"""
    note_text = models.TextField()
    project = models.ForeignKey(Task, on_delete=models.CASCADE)
    task = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
"""
class NoteForm(ModelForm):

    class Meta:
        model = Note
        fields = ['note_text']
