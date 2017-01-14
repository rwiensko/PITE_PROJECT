import hashlib
import random

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile
from accounts.views import add_friend, register, activation
from django.test.client import RequestFactory


class TestModels(TestCase):

    def setUp(self):
        self.profile = Profile()
        self.profile.user = User.objects.create_user('user1','test@test.pl','test')
        self.profile.save()
        self.friend_profile = Profile()
        self.friend_profile.user = User.objects.create_user('user2','test@test.pl','test')

    def test_set_up(self):
        self.assertEqual(self.profile.user.username,'user1')
        self.assertEqual(self.profile.user.email, 'test@test.pl')

    def test_add_friend(self):

        self.profile.list_of_friends = []
        self.profile.add_friend(self.friend_profile.user.id)

        self.assertEquals([self.friend_profile.user.id], self.profile.list_of_friends)


class TestViews(TestCase):

    def setUp(self):

        self.user = User.objects.create_user('user2', 'test@test.pl','test')
        self.friend = User.objects.create_user('user3', 'test@test.pl', 'test')
        self.user_profile = Profile()
        self.user_profile.user = self.user
        self.friend_profile = Profile()
        self.friend_profile.user = self.friend
        self.user_profile.is_active = True
        self.friend_profile.is_active = True
        self.friend_profile.save()
        self.user_profile.save()
        self.factory = RequestFactory()

    def test_add_friend(self):

        user_id = self.user.id
        friend_id = self.friend.id
        request = self.factory.post('home.html',{'user': user_id})
        add_friend(request, friend_id)
        friend_profile = Profile.objects.get(user=self.friend)
        user_profile = Profile.objects.get(user=self.user)
        self.assertEqual([user_id], friend_profile.list_of_friends)
        self.assertEqual([friend_id], user_profile.list_of_friends)

    def test_register(self):

        user = User.objects.create_user('user4', 'test@test.pl', 'test')
        request = self.factory.post('home.html',{'user': user.id})
        request.user = user
        register(request)

        self.assertEqual(user,User.objects.get(id=user.id))

    def test_activation(self):

        profile = Profile()
        user = User.objects.create_user('user4', 'test@test.pl', 'test')
        user.is_active = False
        user.save()
        profile.user = user
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        user_name_salt = user.username.encode('utf8')
        activation_key = hashlib.sha1(salt + user_name_salt).hexdigest()
        request = self.factory.post('home.html',{'user': user.id})
        profile.activation_key = activation_key
        profile.save()

        self.assertEqual(User.objects.get(id=profile.user.id).is_active,False)

        activation(request, activation_key)

        self.assertEqual(User.objects.get(id=profile.user.id).is_active,True)