from django.test import TestCase

from datetime import datetime
from django.contrib.auth.models import User

from accounts.models import Profile


class TestAccounts(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test','test@test.pl','test')
        self.profile = Profile(self.user,[],'test',datetime.today())

    def test_set_up(self):
        self.assertEqual(self.user.username,'test')