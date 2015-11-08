# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import messages
from django.db import IntegrityError
from models import Bucketlist
import datetime


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class RootView(View):
    template_name = "website/index.html"

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        return render(
                request, self.template_name,
                {
                    'today': today,
                    'now': now(),
                    'page_title': 'Home'
                }
            )


class RootFilesView(View):
    """Renders requests for `robots.txt` and `humans.txt`"""

    def get(self, request, *args, **kwargs):
        return render(
            request, self.kwargs.get('filename'),
            {}, content_type="text/plain"
        )


class LoginView(View):
    """Renders requests for authorization.
    """
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                if not user.check_password(password):
                    messages.error(request, 'Wrong username or password.')
                    return redirect(
                        reverse('app.index'))
                else:
                    user = authenticate(
                        username=user.username,
                        password=user.password)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(
                username=username,
                password=password)
        if user is not None:
            login(request, user)
            return redirect(
                reverse('app.dashboard'))

        messages.error(request, 'Wrong username or password.')
        return redirect(
                reverse('app.index'))


class LogoutView(View):
    """Renders request to logout authenticated session.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('app.index'))


class SignUpView(View):
    """Processes request to signup a user
    """
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        username = request.POST.get('username')
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
        except IntegrityError:
            messages.error(request, 'Username is already taken.')
            return redirect(reverse('app.index'))

        if user:
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request,
                'Hello {}, please kindly update \
                your profile information.'.format(first_name))
            return redirect(reverse('app.dashboard'))
        return redirect(reverse('app.login'))


class DashboardView(LoginRequiredMixin, View):
    """Renders dashboard for logged in user"""

    def get(self, request, *arg, **kwargs):
        return render(
            request,
            'website/dashboard.html', {}
            )


class BucketlistView(LoginRequiredMixin, View):
    """Renders bucketlist for logged in user"""

    def post(self, request, *arg, **kwargs):
        name = request.POST.get('name')
        user = request.user
        bucketlist = Bucketlist(name=name, user=user)
        bucketlist.save()
        messages.success(
            request,
            'Bucketlist has been added successfully')
        return redirect(reverse('app.dashboard'))        
