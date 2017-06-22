from django.test import TestCase

from portal.forms import SignUpForm


def create_form(username):
    form_data = {'username': username}
    return SignUpForm(data=form_data)


class SignUpFormTests(TestCase):
    def test_empty_form_is_invalid(self):
        form = create_form('')
        self.assertFalse(form.is_valid())

    def test_maximum_username_length(self):
        form = create_form('ab123415')
        self.assertFalse(form.is_valid())

        form = create_form('ab12315')
        self.assertTrue(form.is_valid())