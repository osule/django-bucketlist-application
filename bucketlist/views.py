# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.utils.timezone import now
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
    """This view renders requests for `robots.txt` and `humans.txt`"""

    def get(self, request, *args, **kwargs):
        return render(
            request, self.kwargs.get('filename'),
            {}, content_type="text/plain"
        )
