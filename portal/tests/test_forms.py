from django.test import TestCase

from portal.forms import SignUpForm, PreferenceForm
from portal.models import Hobby


class SignUpFormTests(TestCase):
    @staticmethod
    def create_form(username=''):
        form_data = {'username': username}
        return SignUpForm(data=form_data)

    def test_empty_form_is_invalid(self):
        form = self.create_form()
        self.assertFalse(form.is_valid())

    def test_maximum_username_length(self):
        form = self.create_form('ab123415')
        self.assertFalse(form.is_valid())

        form = self.create_form('ab12315')
        self.assertTrue(form.is_valid())


class PreferenceFormTests(TestCase):
    @staticmethod
    def create_form(does_party=False, hobbies=None):
        form_data = {'party': does_party, 'hobbies': hobbies}
        return PreferenceForm(data=form_data)

    def test_empty_is_valid(self):
        form = self.create_form()
        self.assertTrue(form.is_valid())

    def test_maximum_5_hobbies(self):
        Hobby(description='A').save()
        Hobby(description='B').save()
        Hobby(description='C').save()
        Hobby(description='D').save()
        Hobby(description='E').save()

        form = self.create_form(False, Hobby.objects.all())
        self.assertTrue(form.is_valid())

        Hobby(description='F').save()

        form = self.create_form(False, Hobby.objects.all())
        self.assertFalse(form.is_valid())
