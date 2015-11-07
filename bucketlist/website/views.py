# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
import datetime


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
    template_name = "website/login.html"

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {}
        )

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        user = authenticate(
            username=username,
            password=password)
        if user is not None:
            return redirect(reverse('app.dashboard'))
        else:
            messages.error(request, 'Wrong username or password.')
            return redirect(
                reverse('app.login'))


class LogoutView(View):
    """Renders request to logout authenticated session.
    """
    def get(self, request, *args, **kwargs):
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
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        if user:
            authenticate(username=username, password=password)
            messages.success(
                request,
                'Hello {}, please kindly update your profile information.')
            return redirect(reverse('app.dashboard'))
        return redirect(reverse('app.login'))


class DashboardView(View):
    """Renders dashboard for logged in user"""
    def get(self, request, *arg, **kwargs):
        if request.user.is_authenticated():
            return render(
                request,
                'bucketlist/dashboard.html', {}
            )
