import hashlib
import random
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils import timezone

from accounts.forms import RegistrationForm
from accounts.models import Profile


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/register.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    return render_to_response(
        'home.html',
        {'user': request.user}
    )


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
    return render(request, 'siteApp/activation.html', locals())


def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas = {}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        datas['username'] = user.username
        datas['email'] = user.email
        datas['email_path'] = "/ResendEmail.txt"
        datas['email_subject'] = "New activation link your domain"

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key'] = hashlib.sha1(salt+usernamesalt).hexdigest()

        profile = Profile.objects.get(user=user)
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()

        form.sendEmail(datas)
        request.session['new_link'] = True

    return redirect(home)
