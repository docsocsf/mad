from django.test import TestCase

from portal.mailservice.mailer import Mailer
from portal.mailservice.message import Message
from portal.tests.test_views import create_student_and_return


class MessageTests(TestCase):
    def setUp(self):
        self.student = create_student_and_return(username='ba123', name='Bob')

    def test_cannot_have_empty_subject_or_body(self):
        try:
            message = Message(self.student, '', '')
        except:
            self.assertTrue(True)
            return

        self.assertFalse(True)

    def test_recipient_is_ic_ac_uk(self):
        message = Message(self.student, '_', '_')
        self.assertTrue("ba123@ic.ac.uk" in message.recipient())

    def test_message_contains_name(self):
        message = Message(self.student, '_', '_')
        self.assertTrue("Bob" in message.message())


class MailerTests(TestCase):
    def test_can_disable_sending_emails_for_testing(self):
        with Mailer(False) as mailer:
            # If true it would crash here
            mailer.send_email(None)
        self.assertTrue(True)
