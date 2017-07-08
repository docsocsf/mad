from django.test import TestCase

from portal.models import Family, Hobby, Student
from portal.tests.test_views import create_student_and_return
from portal.utils import create_families_from_parents, assign_children_to_families


def create_family_and_return():
    return Family.objects.create_family()


def create_hobby_and_return(description):
    hobby = Hobby(description=description)
    hobby.save()
    return hobby


def refresh_object(model, obj):
    """
    if changes are made to the database they wont be reflected in the object we hold in memory therefore if we want to
    check if a change has been applied we have to refresh the object in memory.
    """
    return model.objects.get(id=obj.id)


class AssignmentTests(TestCase):
    def test_pair_up_parents_already_paired_does_nothing(self):
        s1 = create_student_and_return('A', child=False, party=True)
        s2 = create_student_and_return('B', child=False, party=True)

        s1.assign_partner(s2)

        create_families_from_parents()

        s1 = refresh_object(Student, s1)
        s2 = refresh_object(Student, s2)

        self.assertEqual(s1.partner, s2)
        self.assertEqual(s2.partner, s1)

    def test_pair_up_not_confirmed_auto_assigns(self):
        s1 = create_student_and_return('A', child=False, party=True)
        s2 = create_student_and_return('B', child=False, party=True)
        s3 = create_student_and_return('C', child=False, party=False)
        s4 = create_student_and_return('D', child=False, party=False)

        s1.partner = s3

        create_families_from_parents()

        s1 = refresh_object(Student, s1)
        s2 = refresh_object(Student, s2)
        s3 = refresh_object(Student, s3)
        s4 = refresh_object(Student, s4)

        self.assertEqual(s1.partner, s2)
        self.assertEqual(s1.confirmed, True)
        self.assertEqual(s2.partner, s1)
        self.assertEqual(s2.confirmed, True)
        self.assertEqual(s3.partner, s4)
        self.assertEqual(s4.partner, s3)

    def test_create_families_from_parent_removes_odd_count(self):
        create_student_and_return('A', child=False)

        create_families_from_parents()

        self.assertEqual(Student.objects.all().count(), 0)

    def test_create_families_children_do_not_get_paired(self):
        create_student_and_return('A', child=True)
        create_student_and_return('B', child=True)

        create_families_from_parents()

        count = Student.objects.filter(confirmed=False, partner__isnull=True).count()
        self.assertEqual(count, 2)

    def test_create_families_assigns_all(self):
        create_student_and_return('A', child=False)
        create_student_and_return('B', child=False)
        create_student_and_return('C', child=False)
        create_student_and_return('D', child=False)

        create_families_from_parents()

        count = Student.objects.filter(confirmed=True, partner__isnull=False).count()
        self.assertEqual(count, 4)

    def test_assign_(self):
        p1 = create_student_and_return('P1', child=False)
        p2 = create_student_and_return('P2', child=False)
        p3 = create_student_and_return('P3', child=False)
        p4 = create_student_and_return('P4', child=False)

        h1 = create_hobby_and_return('A')
        h2 = create_hobby_and_return('B')

        p1.hobbies.add(h1.id)
        p2.hobbies.add(h2.id, h1.id)
        p3.hobbies.add(h2.id)
        p4.hobbies.add(h2.id)

        create_families_from_parents()

        p1 = refresh_object(Student, p1)
        p3 = refresh_object(Student, p3)

        self.assertEqual(p1.partner, p2)
        self.assertEqual(p3.partner, p4)

        s1 = create_student_and_return('S1', child=True)
        s2 = create_student_and_return('S2', child=True)

        s1.hobbies.add(h1.id, h2.id)
        s2.hobbies.add(h2.id)

        assign_children_to_families()

        s1 = refresh_object(Student, s1)
        s2 = refresh_object(Student, s2)

        f1 = Family.objects.get(id=1)
        f2 = Family.objects.get(id=2)

        self.assertTrue(s1 in f1.children.all())
        self.assertTrue(s2 in f2.children.all())

    def test_children_dont_get_reasigned(self):
        p1 = create_student_and_return('P1', child=False)
        p2 = create_student_and_return('P2', child=False)

        h1 = create_hobby_and_return('A')

        create_families_from_parents()

        s1 = create_student_and_return('S1', child=True)
        s1.hobbies.add(h1.id)

        assign_children_to_families()

        f1 = Family.objects.get(id=1)

        s1 = refresh_object(Student, s1)

        self.assertTrue(s1 in f1.children.all())
        self.assertTrue(s1.confirmed)

        p3 = create_student_and_return('P3', child=False)
        p4 = create_student_and_return('P4', child=False)
        p3.hobbies.add(h1.id)
        p4.hobbies.add(h1.id)

        create_families_from_parents()
        assign_children_to_families()

        f2 = Family.objects.get(id=2)

        self.assertFalse(s1 in f2.children.all())
