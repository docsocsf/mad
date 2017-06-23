from django.db import models

from common.util.generator import get_random_id


class Student(models.Model):
    username = models.CharField(max_length=7,unique=True)
    magic_id = models.CharField(max_length=8)
    child = models.BooleanField()

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
