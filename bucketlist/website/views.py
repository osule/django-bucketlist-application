# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.contrib.auth import authenticate
from django.contrib import messages
import datetime


class RootView(View):
    template_name = "bucketlist/index.html"

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        return render(
                request, self.template_name,
                {'today': today, 'now': now()}
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
    template_name = "bucketlist/login.html"

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {}
        )

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
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


class DashboardView(View):
    """Renders dashboard for logged in user"""
    def get(self, request, *arg, **kwargs):
        if request.user.is_authenticated():
            return render(
                request,
                'bucketlist/dashboard.html', {}
            )
