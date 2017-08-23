from math import ceil

from config import POINTS_FOR_PARTY_MATCH, POINTS_FOR_INTEREST_MATCH, EXPECTED_CHILDREN
from portal.models import Student, Family


def get_invalid_id_popup():
    return {'message': "The ID provided is invalid.", 'state': 'danger'}


def get_student_does_not_exist_popup():
    return {'message': "Failed to find student.", 'state': 'danger'}

def get_on_save_wait_popup():
    return {'message': "Preferences saved. Now just wait to be allocated to a family!", 'state': 'success'}


def create_families_from_parents():
    if Student.objects.filter(child=False).count() % 2 != 0:
        to_remove = Student.objects.filter(child=False, partner__isnull=True).last()
        # ToDO(martinzlocha): Inform student that he cant be a parent because there is an odd number and he was last
        to_remove.delete()

    __pair_up_parents()

    paired = list(Student.objects.filter(child=False, partner__isnull=False, confirmed=True))

    for _ in range(int(len(paired) / 2)):
        parent1 = paired[0]
        parent2 = parent1.partner

        paired.remove(parent1)
        paired.remove(parent2)

        Family.objects.create_family(parents=[parent1, parent2])


def assign_children_to_families():
    families = Family.objects.all()
    children = Student.objects.filter(child=True, confirmed=False)

    for child in children:
        __find_family_for_child(child, families)


def __pair_up_parents():
    unconfirmed = list(Student.objects.filter(child=False, confirmed=False))

    while unconfirmed:
        parent1 = unconfirmed[0]
        unconfirmed = unconfirmed[1:]
        parent2 = __find_best_partner_match(parent1, unconfirmed)
        unconfirmed.remove(parent2)
        parent1.assign_partner(parent2)


def __find_best_partner_match(person, others):
    partner = None
    points = -1

    for other in others:
        other_points = __interest_overlap_between_people(person, other)
        if points < other_points:
            points = other_points
            partner = other

    return partner


def __interest_overlap_between_people(person1, person2):
    points = 0

    if person1.party == person2.party:
        points += POINTS_FOR_PARTY_MATCH

    hobbies1 = list(person1.hobbies.all())
    hobbies2 = list(person2.hobbies.all())

    points += len(list(set(hobbies1) & set(hobbies2))) * POINTS_FOR_INTEREST_MATCH

    return points


def __find_family_for_child(child, families):
    use_family = None
    points = -1
    avg_size = __avg_family_size()

    for family in families:
        family_points = __interest_overlap_in_family(child, family, avg_size)
        if points < family_points:
            points = family_points
            use_family = family

    use_family.assign_child(child)


def __interest_overlap_in_family(child, family, avg_size):
    parents = family.parents.all()
    points = 0

    for parent in parents:
        points += __interest_overlap_between_people(child, parent)

    points /= len(parents)
    overflow = max(family.children.count() + 2 - avg_size, 1)
    return points / overflow


def __avg_family_size():
    return ceil(EXPECTED_CHILDREN / max(Family.objects.all().count(), 1))
