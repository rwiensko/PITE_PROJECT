from datetime import datetime
from django.core.mail import send_mail

from django.conf.global_settings import MEDIA_ROOT

from django import forms
from django.contrib.auth.models import User
from django.template import Context
from django.template import Template

from django.utils.translation import ugettext_lazy as _

from accounts.models import Profile


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

    def save(self, datas):
        u = User.objects.create_user(datas['username'],
                                     datas['email'],
                                     datas['password1'])
        u.is_active = False
        u.save()
        profile=Profile()
        profile.user=u
        profile.activation_key=datas['activation_key']
        profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()
        return u

    def sendEmail(self, datas):
        link = "http://yourdomain.com/activate/" + datas['activation_key']
        c = Context({'activation_link': link, 'username': datas['username']})
        f = open(MEDIA_ROOT + datas['email_path'], 'r')
        t = Template(f.read())
        f.close()
        message = t.render(c)
        # print unicode(message).encode('utf8')
        send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']],fail_silently=False)