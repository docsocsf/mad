from django.db import models

from common.util.generator import get_random_id


class Hobby(models.Model):
    description = models.CharField(max_length=300)

    class Meta:
        pass
        # ToDo(martinzlocha): Set the correct plural name to be shown in admin page

    def __str__(self):
        return self.description


class Student(models.Model):
    username = models.CharField(max_length=7,unique=True)
    magic_id = models.CharField(max_length=8)
    child = models.BooleanField()
    party = models.BooleanField(default=False)
    hobbies = models.ManyToManyField(to=Hobby, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if len(self.magic_id) == 0:
            self.magic_id = get_random_id()
        super(Student, self).save(*args, **kwargs)

    def get_new_student_popup(self):
        message = "Email has been sent to %s@ic.ac.uk. Go activate your account." % self.username
        return {'message': message, 'state': 'success'}

    def get_existing_student_popup(self):
        message = "Account already exists. Activation email re-sent to %s@ic.ac.uk." % self.username
        return {'message': message, 'state': 'warning'}
