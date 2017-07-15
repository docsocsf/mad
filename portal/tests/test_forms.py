from django.test import TestCase

from portal.forms import SignUpForm, PreferenceForm, PartnerForm
from portal.models import Hobby
from portal.tests.test_views import create_student_and_return


class SignUpFormTests(TestCase):
    @staticmethod
    def create_form(username=''):
        form_data = {'name': 'Name', 'username': username, 'gender': 'M', 'course': 'C'}
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


class PartnerFormTests(TestCase):
    @staticmethod
    def create_form(instance=None, partner=None):
        if not partner:
            form_data = {}
        else:
            form_data = {'partner': partner.id}
        return PartnerForm(instance=instance, data=form_data)

    def setUp(self):
        self.student = create_student_and_return('A', child=False)

    def test_empty_form_is_valid(self):
        form = self.create_form(self.student)
        self.assertTrue(form.is_valid())

    def test_propose_to_someone_else_is_valid(self):
        new = create_student_and_return('B', child=False)
        form = self.create_form(self.student, new)
        self.assertTrue(form.is_valid())

    def test_student_cant_propose_to_self(self):
        form = self.create_form(self.student, self.student)
        self.assertFalse(form.is_valid())

    def test_cannot_propose_to_child(self):
        new = create_student_and_return('B', child=True)
        form = self.create_form(self.student, new)
        self.assertFalse(form.is_valid())

    def test_cannnot_propose_to_someone_married(self):
        new = create_student_and_return('B', child=False)
        new.confirmed = True
        new.save()
        form = self.create_form(self.student, new)
        self.assertFalse(form.is_valid())
