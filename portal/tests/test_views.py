from django.test import TestCase
from django.urls import reverse

from common.util.generator import get_random_id
from portal.models import Student, Hobby
from portal.tests.constants import VALID_USERNAME
from portal.utils import get_invalid_id_popup


def create_student_and_return(username='Test', child=True, magic_id=None):
    if magic_id is None:
        magic_id = get_random_id()

    student = Student(username=username, child=child,  magic_id=magic_id)
    student.save()
    return student


def create_hobby(description):
    Hobby(description=description).save()


class IndexViewTests(TestCase):
    DEFAULT = reverse('portal:index')
    PARENT = reverse('portal:index', kwargs={'position': 'parent'})
    CHILD = reverse('portal:index', kwargs={'position': 'child'})

    def test_index_returns_child_submission(self):
        response = self.client.get(self.DEFAULT)
        self.assertContains(response, 'child')

    def test_child_page_correctly_returned(self):
        response = self.client.get(self.CHILD)
        self.assertContains(response, 'child')

    def test_parent_page_correctly_returned(self):
        response = self.client.get(self.PARENT)
        self.assertContains(response, 'parent')

    def test_child_created_correctly(self):
        response = self.client.post(self.CHILD, {'username': VALID_USERNAME})
        self.assertTrue(Student.objects.filter(username=VALID_USERNAME).exists())

        student = Student.objects.get(username=VALID_USERNAME)
        self.assertTrue(student.child)

        self.assertContains(response, student.get_new_student_popup()['message'])

    def test_parent_created_correctly(self):
        self.client.post(self.PARENT, {'username': VALID_USERNAME})
        self.assertTrue(Student.objects.filter(username=VALID_USERNAME).exists())


class PreferenceViewTests(TestCase):
    @staticmethod
    def get_preferences_url(magic_id):
        return reverse('portal:preferences', kwargs={'id': magic_id})

    def test_invalid_id_sends_to_index(self):
        response = self.client.get(self.get_preferences_url('12345678'))
        self.assertContains(response, get_invalid_id_popup()['message'])
        self.assertContains(response, 'Register')

    def test_correctly_returns_saved_data(self):
        magic_id = '12345678'

        student = create_student_and_return(magic_id=magic_id)
        create_hobby('A')
        create_hobby('B')
        create_hobby('C')

        response = self.client.get(self.get_preferences_url(magic_id))
        self.assertNotContains(response, 'checked')

        student.party = True
        student.save()

        response = self.client.get(self.get_preferences_url(magic_id))
        self.assertContains(response, 'checked')

        student.party = False
        student.hobbies = Hobby.objects.filter(description='A')
        student.save()

        response = self.client.get(self.get_preferences_url(magic_id))
        self.assertContains(response, 'checked')
