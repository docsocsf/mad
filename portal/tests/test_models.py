from django.test import TestCase

from portal.models import Student
from portal.tests.constants import VALID_USERNAME


class StudentModelTests(TestCase):
    def test_save_sets_magic_id(self):
        student = Student(username=VALID_USERNAME, child=True)
        student.save()
        self.assertNotEqual(student.magic_id, "")
        self.assertEqual(len(student.magic_id), 8)

    def test_popup_contains_username(self):
        student = Student(username=VALID_USERNAME, magic_id="12345678", child=True)
        student.save()
        self.assertTrue(VALID_USERNAME in student.get_new_student_popup()['message'])
        self.assertTrue(VALID_USERNAME in student.get_existing_student_popup()['message'])