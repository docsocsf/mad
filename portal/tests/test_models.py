from django.test import TestCase

from portal.models import Student
from portal.tests.constants import VALID_USERNAME


def success(response):
    return response['state'] == 'success'


class StudentModelTests(TestCase):
    def setUp(self):
        self.parent1 = Student(username='A', child=False)
        self.parent2 = Student(username='B', child=False)
        self.parent3 = Student(username='C', child=False)

        self.parent1.save()
        self.parent2.save()
        self.parent3.save()

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

    def test_successful_marriage(self):
        self.parent1.partner = self.parent2
        self.assertTrue(success(self.parent2.marry_to(self.parent1)))
        self.assertEqual(self.parent1.partner, self.parent2)
        self.assertEqual(self.parent2.partner, self.parent1)
        self.assertTrue(self.parent1.confirmed)
        self.assertTrue(self.parent2.confirmed)

    def test_protected_against_unrequested_marriage(self):
        self.assertFalse(success(self.parent1.marry_to(self.parent2)))
        self.assertFalse(self.parent2.confirmed)
        self.assertNotEqual(self.parent2.partner, self.parent1)

    def test_protect_double_marriage(self):
        self.parent2.partner = self.parent1
        self.parent3.partner = self.parent1
        self.assertTrue(success(self.parent1.marry_to(self.parent2)))
        self.assertFalse(success(self.parent1.marry_to(self.parent3)))
        self.assertEqual(self.parent1.partner, self.parent2)

    def test_cannot_marry_in_triangle(self):
        self.parent1.partner = self.parent2
        self.parent2.partner = self.parent3
        self.assertTrue(success(self.parent2.marry_to(self.parent1)))
        self.assertFalse(success(self.parent3.marry_to(self.parent2)))
        self.assertEqual(self.parent1.partner, self.parent2)
        self.assertEqual(self.parent2.partner, self.parent1)
        self.assertFalse(self.parent3.confirmed)

    def test_can_withdraw_before_marriage(self):
        self.parent1.partner = self.parent2
        self.assertTrue(success(self.parent1.withdraw_proposal()))

    def test_cannot_withdraw_if_not_proposed(self):
        self.assertFalse(success(self.parent1.withdraw_proposal()))

    def test_cannot_withdraw_once_married(self):
        self.parent1.partner = self.parent2
        self.assertTrue(success(self.parent2.marry_to(self.parent1)))
        self.assertFalse(success(self.parent1.withdraw_proposal()))

    def test_cannot_reject_if_not_proposed(self):
        self.assertFalse(success(self.parent2.reject_proposal(self.parent1)))

    def test_cannot_marry_after_reject(self):
        self.parent1.partner = self.parent2
        self.assertTrue(success(self.parent2.reject_proposal(self.parent1)))
        self.assertFalse(success(self.parent2.marry_to(self.parent1)))
        self.assertNotEqual(self.parent1.partner, self.parent2)

    def test_cannot_reject_once_accepted(self):
        self.parent1.partner = self.parent2
        self.assertTrue(success(self.parent2.marry_to(self.parent1)))
        self.assertFalse(success(self.parent2.reject_proposal(self.parent1)))
