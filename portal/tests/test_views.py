from django.test import TestCase
from django.urls import reverse

from portal.models import Student, Hobby
from portal.tests.constants import VALID_USERNAME
from portal.utils import get_invalid_id_popup, create_families_from_parents, assign_children_to_families


def create_student_and_return(username, child=False, magic_id=None, party=False, name='Name', gender='M', course='C'):
    student = Student(username=username, child=child,  magic_id=magic_id, party=party, name=name, gender=gender,
                      course=course)

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

    def test_child_registration_closed(self):
        response = self.client.post(self.CHILD,
                                    {'name': 'Name', 'username': VALID_USERNAME, 'gender': 'M', 'course': 'C'})
        self.assertFalse(Student.objects.filter(username=VALID_USERNAME).exists())
        self.assertContains(response, "closed")

    def test_parent_created_correctly(self):
        self.client.post(self.PARENT, {'name': 'Name', 'username': VALID_USERNAME, 'gender': 'M', 'course': 'C'})
        self.assertTrue(Student.objects.filter(username=VALID_USERNAME).exists())

    def test_cannot_create_same_account_twice(self):
        response = self.client.post(self.PARENT,
                                    {'name': 'Name', 'username': VALID_USERNAME, 'gender': 'M', 'course': 'C'})
        self.assertContains(response, "activate")

        response = self.client.post(self.PARENT,
                                    {'name': 'Name', 'username': VALID_USERNAME, 'gender': 'M', 'course': 'C'})
        self.assertContains(response, "exists")
        self.assertTrue(Student.objects.filter(username=VALID_USERNAME).count() == 1)

    def test_account_not_activated_when_created(self):
        self.client.post(self.PARENT, {'name': 'Name', 'username': VALID_USERNAME, 'gender': 'M', 'course': 'C'})

        student = Student.objects.get(username=VALID_USERNAME)
        self.assertFalse(student.activated)


class PreferenceViewTests(TestCase):
    def setUp(self):
        self.student1 = create_student_and_return('A', name='A')
        self.student2 = create_student_and_return('B', name='B')

    def refreshSetUp(self):
        self.student1 = Student.objects.get(id=self.student1.id)
        self.student2 = Student.objects.get(id=self.student2.id)

    @staticmethod
    def get_preferences_url(magic_id):
        return reverse('portal:preferences', kwargs={'id': magic_id})

    def test_invalid_id_sends_to_index(self):
        response = self.client.get(self.get_preferences_url('12345678'))
        self.assertContains(response, "closed")

    def test_correctly_returns_saved_data(self):
        create_hobby('A')
        create_hobby('B')
        create_hobby('C')

        response = self.client.get(self.get_preferences_url(self.student1.magic_id))
        self.assertNotContains(response, 'checked')

        self.student1.party = True
        self.student1.save()

        response = self.client.get(self.get_preferences_url(self.student1.magic_id))
        self.assertContains(response, 'checked')

        self.student1.party = False
        self.student1.hobbies = Hobby.objects.filter(description='A')
        self.student1.save()

        response = self.client.get(self.get_preferences_url(self.student1.magic_id))
        self.assertContains(response, 'checked')

    def test_can_select_preferred_partner(self):
        response = self.client.post(self.get_preferences_url(self.student1.magic_id), {'partner': self.student2.id})
        self.assertContains(response, self.student2.username)
        self.assertContains(response, 'success')

        self.student1 = Student.objects.get(id=self.student1.id)
        self.assertEqual(self.student1.partner, self.student2)

    def test_children_cant_select_partner(self):
        self.student1 = create_student_and_return('C', child=True)
        response = self.client.get(self.get_preferences_url(self.student1.magic_id))
        self.assertNotContains(response, 'form-partner')

    def test_parent_can_select_partner(self):
        response = self.client.get(self.get_preferences_url(self.student1.magic_id))
        self.assertContains(response, 'form-partner')

    def test_empty_post_is_handled(self):
        try:
            self.client.post(self.get_preferences_url(self.student1.magic_id))
        except:
            self.assertTrue(False)

    def test_can_accept_proposal(self):
        self.client.post(self.get_preferences_url(self.student1.magic_id), {'partner': self.student2.id})
        response = self.client.get(self.get_preferences_url(self.student2.magic_id))

        self.assertContains(response, self.student1.username)
        self.assertContains(response, 'accept')

        response = self.client.post(self.get_preferences_url(self.student2.magic_id),
                                    {'username': self.student1.username, 'accept': ''})
        self.assertContains(response, self.student1.username)
        self.assertContains(response, 'married')

        self.refreshSetUp()

        self.assertTrue(self.student1.confirmed)
        self.assertTrue(self.student2.confirmed)

    def test_cannot_withdraw_after_reject(self):
        self.client.post(self.get_preferences_url(self.student1.magic_id), {'partner': self.student2.id})
        self.client.post(self.get_preferences_url(self.student2.magic_id),
                         {'username': self.student1.username, 'reject': ''})

        self.refreshSetUp()

        self.assertNotEqual(self.student1.partner, self.student2)
        self.assertNotEqual(self.student2.partner, self.student1)

        response = self.client.post(self.get_preferences_url(self.student1.magic_id),
                                    {'username': self.student2.username, 'withdraw': ''})

        self.assertContains(response, 'danger')

    def test_cannot_propose_twice(self):
        self.student3 = create_student_and_return('C')
        self.client.post(self.get_preferences_url(self.student1.magic_id), {'partner': self.student2.id})
        self.client.post(self.get_preferences_url(self.student1.magic_id), {'partner': self.student3.id})
        self.refreshSetUp()
        self.assertEqual(self.student1.partner, self.student2)

    def test_cannot_reject_twice(self):
        self.client.post(self.get_preferences_url(self.student1.magic_id), {'partner': self.student2.id})
        response = self.client.post(self.get_preferences_url(self.student1.magic_id),
                                    {'username': self.student2.username, 'withdraw': ''})
        self.assertContains(response, 'success')
        self.assertNotContains(response, 'danger')

        response = self.client.post(self.get_preferences_url(self.student1.magic_id),
                                    {'username': self.student2.username, 'withdraw': ''})
        self.assertContains(response, 'danger')
        self.assertNotContains(response, 'success')

    def test_cannot_withdraw_twice(self):
        self.client.post(self.get_preferences_url(self.student1.magic_id), {'partner': self.student2.id})
        response = self.client.post(self.get_preferences_url(self.student2.magic_id),
                                    {'username': self.student1.username, 'reject': ''})
        self.assertContains(response, 'success')
        self.assertNotContains(response, 'danger')

        response = self.client.post(self.get_preferences_url(self.student2.magic_id),
                                    {'username': self.student1.username, 'reject': ''})
        self.assertContains(response, 'danger')
        self.assertNotContains(response, 'success')

    def test_cannot_accept_twice(self):
        self.client.post(self.get_preferences_url(self.student1.magic_id), {'partner': self.student2.id})
        response = self.client.post(self.get_preferences_url(self.student2.magic_id),
                                    {'username': self.student1.username, 'accept': ''})
        self.assertContains(response, 'success')
        self.assertNotContains(response, 'danger')

        response = self.client.post(self.get_preferences_url(self.student2.magic_id),
                                    {'username': self.student1.username, 'accept': ''})
        self.assertContains(response, 'danger')
        self.assertNotContains(response, 'success')

    def test_shows_parents_and_children_after_assignment(self):
        child = create_student_and_return('child', child=True)
        create_families_from_parents()
        assign_children_to_families()
        response = self.client.get(self.get_preferences_url(child.magic_id))
        self.assertContains(response, self.student1)
        self.assertContains(response, self.student2)

        response = self.client.get(self.get_preferences_url(self.student1.magic_id))
        self.assertContains(response, child)

    def test_account_gets_activated_after_visit(self):
        self.client.get(self.get_preferences_url(self.student1.magic_id))
        student = Student.objects.get(id=self.student1.id)
        self.assertTrue(student.activated)
