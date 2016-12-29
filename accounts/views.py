import hashlib
import random
from datetime import datetime
from django.db import transaction, IntegrityError

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from accounts.forms import RegistrationForm
from accounts.models import Profile

import logging

log = logging.getLogger(__name__)


def register(request):
    if request.user.is_authenticated():
        return redirect(home)
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data={}
            data['username'] = form.cleaned_data['username']
            data['email'] = form.cleaned_data['email']
            data['password1'] = form.cleaned_data['password1']

            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            user_name_salt = data['username']
            if isinstance(user_name_salt, unicode):
                user_name_salt = user_name_salt.encode('utf8')
            data['activation_key'] = hashlib.sha1(salt+user_name_salt).hexdigest()
            data['email_subject'] = "Activation mail"
            data['host_name'] = request.get_host()
            form.sendEmail(data)
            form.save(data)

            request.session['registered']=True
            return redirect(home)
        else:
            registration_form = form
    return render(request, 'registration/register.html', locals())


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    return render_to_response('home.html',{'user': request.user})


def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if not profile.user.is_active:
        if timezone.now() > profile.key_expires:
            activation_expired = True
            id_user = profile.user.id
        else:
            profile.user.is_active = True
            profile.user.save()

    else:
        already_active = True
    return render(request, 'registration/success.html', locals())


def new_activation_link(request, user_id):
    form = RegistrationForm()
    data = {}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        data['username'] = user.username
        data['email'] = user.email
        data['email_subject'] = "New activation link"

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        user_name_salt = data['username']
        if isinstance(user_name_salt, unicode):
            user_name_salt = user_name_salt.encode('utf8')
        data['activation_key'] = hashlib.sha1(salt+user_name_salt).hexdigest()

        profile = Profile.objects.get(user=user)
        profile.activation_key = data['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.list_of_friends = []
        profile.save()

        form.sendEmail(data)
        request.session['new_link'] = True

    return redirect(home)


def add_nothing(request):
    return render_to_response('friends.html', {'user': request.user})


def add_friend(request, friend_id):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST['user'])
        friend = User.objects.get(id=friend_id)
        if user is not None and friend is not None and (user.is_active and friend.is_active):
            user_profile = Profile.objects.get(user=user)
            user_profile.add_friend(friend_id)
            user_profile.save()
            friend_profile = Profile.objects.get(user=friend)
            friend_profile.add_friend(user.id)
            friend_profile.save()


