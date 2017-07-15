from django.db import models

from common.util.generator import get_random_id
from config import DOMAIN_URL
from portal.mailservice.mailer import Mailer
from portal.mailservice.message import Message


class Hobby(models.Model):
    description = models.CharField(max_length=300)

    class Meta:
        pass
        # ToDo(martinzlocha): Set the correct plural name to be shown in admin page

    def __str__(self):
        return self.description


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Prefer not to say'),
    )

    COURSE_CHOICES = (
        ('C', 'Computing'),
        ('J', 'JMC')
    )

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=7, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    course = models.CharField(max_length=1, choices=COURSE_CHOICES)
    magic_id = models.CharField(max_length=8)
    child = models.BooleanField()
    party = models.BooleanField(default=False)
    hobbies = models.ManyToManyField(to=Hobby, blank=True)
    partner = models.ForeignKey('Student', null=True, blank=True)
    family = models.ForeignKey('Family', null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.magic_id or len(self.magic_id) == 0:
            self.magic_id = get_random_id()
        super(Student, self).save(*args, **kwargs)

    def get_new_student_popup(self):
        popup = "Email has been sent to %s@ic.ac.uk. Please check your email to activate your account." % self.username
        message = "To view the Mums and Dads portal go to %s/preferences/%s/\n\nKeep this URL safe, anyone with it " \
                  "can see your hobbies." % (DOMAIN_URL, self.magic_id)

        with Mailer() as mail:
            mail.send_email(Message(self, "Mums and Dads login link", message))

        return {'message': popup, 'state': 'success'}

    def get_existing_student_popup(self):
        message = "Account already exists. You should have received an email at %s@ic.ac.uk." % self.username
        return {'message': message, 'state': 'warning'}

    def assign_partner(self, partner):
        self.assign_to(self, partner)
        self.assign_to(partner, self)

    def marry_to(self, partner):
        if self.confirmed or partner.partner != self:
            message = "You  cannot marry this person. Might have occurred because %s withdrew their proposal." % partner
            return {'message': message, 'state': 'danger'}

        self.assign_partner(partner)

        message = "You have married %s successfully." % partner
        return {'message': message, 'state': 'success'}

    def withdraw_proposal(self):
        if self.confirmed or not self.partner:
            message = "You cannot withdraw your proposal because %s already accepted. That's rude!" % self.partner
            return {'message': message, 'state': 'danger'}

        self.partner = None
        self.save()

        message = "Your proposal has been withdrawn."
        return {'message': message, 'state': 'success'}

    def reject_proposal(self, partner):
        if self.confirmed or partner.partner != self:
            message = "Failed to reject proposal. Might have been caused because %s withdrew their offer. " % partner
            return {'message': message, 'state': 'danger'}

        partner.partner = None
        partner.save()

        message = "You have successfully rejected %s proposal. Ouch!" % partner
        return {'message': message, 'state': 'success'}

    def activate(self):
        if not self.activated:
            self.activated = True
            self.save()

    @staticmethod
    def assign_to(student, to):
        student.partner = to
        student.confirmed = True
        student.save()


class FamilyManager(models.Manager):
    def create_family(self, parents=None):
        family = self.create()

        if parents:
            for parent in parents:
                family.parents.add(parent.id)
                parent.family = family
                parent.save()

        return family


class Family(models.Model):
    parents = models.ManyToManyField(to=Student, related_name='parents')
    children = models.ManyToManyField(to=Student, related_name='children')

    objects = FamilyManager()

    def __str__(self):
        return str(self.id)

    def assign_child(self, child):
        self.children.add(child.id)
        child.family = self
        child.confirmed = True
        child.save()
