from math import ceil
from random import shuffle

from config import POINTS_FOR_PARTY_MATCH, POINTS_FOR_INTEREST_MATCH, EXPECTED_CHILDREN, DOMAIN_URL
from portal.config.messages import ASSIGNED_PARTNER_TEMPLATE, INACTIVE_ACCOUNT_TEMPLATE, ASSIGNED_TO_FAMILY
from portal.mailservice.mailer import Mailer
from portal.mailservice.message import Message
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
    family_options = list()
    points = -1
    avg_size = __avg_family_size()

    for family in families:
        if __family_can_get_child(child, family):
            family_points = __interest_overlap_in_family(child, family, avg_size)
            if points < family_points:
                points = family_points
                family_options = list()
                family_options.append(family)
            elif points == family_points:
                family_options.append(family)

    shuffle(family_options)

    size = 999
    use_family = None

    for family in family_options:
        if size > family.children.count():
            size = family.children.count()
            use_family = family

    use_family.assign_child(child)


def __family_can_get_child(child, family):
    parents = family.parents.all()

    match_course = False
    match_gender = False

    for parent in parents:
        if parent.course == child.course:
            match_course = True

        if not child.is_female() or parent.is_female():
            match_gender = True

    return match_course and match_gender


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


def email_inactive_accounts():
    students = Student.objects.filter(activated=False).all()

    with Mailer() as mail:
        for student in students:
            message = INACTIVE_ACCOUNT_TEMPLATE % (DOMAIN_URL, student.magic_id)
            mail.send_email(Message(student, "Mums and Dads Account Activation", message))


def notify_family_assignments():
    families = Family.objects.all()

    with Mailer() as mail:
        for family in families:
            parents = family.parents.filter(partner__isnull=False, confirmed=True, emailed=False).all()

            for parent in parents:
                partner = parent.partner
                message = ASSIGNED_PARTNER_TEMPLATE % (partner, partner.username)
                mail.send_email(Message(parent, "Mums and Dads Partner Assignment", message))
                partner.emailed = True
                partner.save()


def notify_child_assignments():
    families = Family.objects.all()

    with Mailer() as mail:
        for family in families:
            parents = family.parents.all()
            children = family.children.filter(emailed=False).all()

            if children.count() > 0:
                for child in children:
                    position = "parents"
                    message = ASSIGNED_TO_FAMILY % (position, position, DOMAIN_URL, child.magic_id)
                    mail.send_email(Message(child, "Mums and Dads Parent Assignment", message))
                    child.emailed = True
                    child.save()

                for parent in parents:
                    position = "children"
                    message = ASSIGNED_TO_FAMILY % (position, position, DOMAIN_URL, parent.magic_id)
                    mail.send_email(Message(parent, "Mums and Dads Child Assignment", message))
