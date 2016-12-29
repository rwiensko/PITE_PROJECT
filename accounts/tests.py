from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile
from accounts.views import add_friend
from django.test.client import RequestFactory


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test','test@test.pl','test')
        self.profile = Profile(self.user,[])

    def test_set_up(self):
        self.assertEqual(self.user.username,'test')


class TestViews(TestCase):

    def setUp(self):

        self.user = User.objects.create_user('test', 'test@test.pl','test')
        self.friend = User.objects.create_user('friend', 'friend@friend.pl', 'friend')
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