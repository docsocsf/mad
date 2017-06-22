from django.test import TestCase

from portal.models import Student
from portal.tests.constants import VALID_USERNAME


class IndexViewTests(TestCase):
    def test_index_returns_child_submission(self):
        response = self.client.get('/')
        self.assertContains(response, 'child')

    def test_child_page_correctly_returned(self):
        response = self.client.get('/child/')
        self.assertContains(response, 'child')

    def test_parent_page_correctly_returned(self):
        response = self.client.get('/parent/')
        self.assertContains(response, 'parent')

    def test_child_created_correctly(self):
        response = self.client.post('/child/', {'username': VALID_USERNAME})
        self.assertTrue(Student.objects.filter(username=VALID_USERNAME).exists())

        student = Student.objects.get(username=VALID_USERNAME)
        self.assertTrue(student.child)

        self.assertContains(response, student.get_new_student_popup()['message'])

    def test_parent_created_correctly(self):
        self.client.post('/parent/', {'username': VALID_USERNAME})
        self.assertTrue(Student.objects.filter(username=VALID_USERNAME).exists())
