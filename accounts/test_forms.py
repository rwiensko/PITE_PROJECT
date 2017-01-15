import hashlib
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from django.forms import ValidationError
from accounts.forms import RegistrationForm
from accounts.models import Profile

class TestForms(TestCase):
    def setUp(self):
        self.form_data = {
            'username': "wojtek",
            'email': "wojtarz@tlen.pl",
            'password1': "marik1234",
            'password2': "marik1234",
            'activation_key': 'kluczAktywacyjny'
        }
        self.form = RegistrationForm(data=self.form_data)

    def test_clean(self):
        wrong_data = {
            'username': "wojtek",
            'email': "wojtarz@tlen.pl",
            'password1': "marik1234",
            'password2': "Mario0000",
            'activation_key': 'kluczAktywacyjny'
        }
        form = RegistrationForm(data=wrong_data)
        form.is_valid()
        with self.assertRaises(ValidationError):
            form.clean()

    def test_save(self):
        self.assertTrue(self.form.is_valid())
        self.form.save(self.form_data)
        profile = Profile.objects.last()
        user = User.objects.last()
        self.assertEqual(1, len(Profile.objects.all()))
        self.assertEqual([], profile.list_of_friends)
        self.assertEqual(profile.user, user)
        self.assertEqual(user.is_active, False)

    def test_sendEmail(self):
        send_email_data = {
            'host_name': 'intense-bastion-41837.herokuapp.com',
            'activation_key': 'kluczAktywacyjny',
            'email_subject': "New activation link",
            'email': self.form_data['email'],
        }
        self.form.sendEmail(send_email_data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "New activation link")
