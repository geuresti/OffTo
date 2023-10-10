from django.test import TestCase

from .forms import LogInForm

from http import HTTPStatus

from .models import Project, Group_Type, Person, Task, Note
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.urls import reverse
from django.test.utils import setup_test_environment # for response.content
from django.test import Client

# model tests have a separate DB that is destroyed after testing (be defautl)
# test command: "python manage.py test <ProjectManager>"
    # can have multiple test files
    # tests are run with Debug = False
#           ASSERTIONS:
#   assertContains(response, "asdasd")
#   assertQuerysetEqual(response.context['sadsada'], [])
#   assertIs(condition, True/False)
#   assertEqual(a, b)
#   assertNotEqual(a,b)
#   assert<True/False>(x)
#   assertIs<Not/None/NotNone>(a,b/x/x)
#   assert<NotIn/In>(a,b)
#   assert(Not)IsInstance(a,b)

class PersonModelTests(TestCase):
    def test_person_model_creation(self):
        person = Person(
            first_name="John",
            last_name="Doe",
            email="my_email@gmail.com"
        )
        self.assertIs(person.first_name, "John")

class UserModelTests(TestCase):

    username = None
    email = None
    password = None
    user = None

    def test_user_creation(self):
        self.username = "user123"
        self.email = "someemail@gmail.com"
        self.password = "pass123"
        test_user = User.objects.create_user(
            self.username,
            self.email,
            self.password
        )

        self.user = User.objects.get(pk=1)

        self.assertIs(self.user==None, False)
        self.assertIs(self.user.username==self.username, True)
        self.assertIs(self.user.email==self.email, True)

    def test_user_authentication(self):
        user_auth_test = authenticate(
            username=self.username,
            password=self.password
        )

        self.assertIs(self.user==user_auth_test, True)

# (client).get(path, data{'a':'b'}, ...)
class AuthFormTests(TestCase):

    client = Client()
    #{"field_name": "value"}
    # self.assertEqual(form.errors[...])

    def test_log_in_get(self):
        url = reverse('log_in')
        response = self.client.get(url)
        #print("\n", response.content, "\n")
        #print("\n STATUS CODE:", response.status_code, "\n")

        self.assertContains(response, "LOG INTO YOUR ACCOUNT")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_form(self):
        username = "a_test_user"
        email = "someemail@gmail.com"
        password = "a_test_password"
        test_user = User.objects.create_user(
            username,
            email,
            password
        )

        form_data = {'username':'a_test_user', 'password':'a_test_password'}
        url = reverse('log_in')
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND) # 302 (redirect*)

    def test_login_form_with_invalid_username(self):
        form_data = {'username':'thisuserisntreal', 'password':'somepassword123'}
        url = reverse('log_in')
        response = self.client.post(url, form_data)

        #print("\n", response.content, "\n")
        #print("\n STATUS CODE:", response.status_code, "\n")
        templates = [template.name for template in response.templates]

        self.assertIn("ProjectManager/log_in.html", templates)
        self.assertContains(response, "* an account with that username does not exist")
        self.assertEqual(response.status_code, HTTPStatus.OK)

# BLOCK CONTENT not rendering (when extending base.html)
#class ViewTests(TestCase):

#    client = Client()

#    def test_index_view(self):
#        response = self.client.get(reverse('index'))
        #print("RESPONSE CODE:", response.status_code)
        #print(response.content)
#        self.assertContains(response, "LOG INTO YOUR ACCOUNT")
