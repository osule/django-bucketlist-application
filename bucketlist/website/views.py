# -*- coding: utf-8 -*-
from django.views.generic import View, ListView, DetailView, \
    CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import TemplateDoesNotExist
from django.http import Http404
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count
from website.models import Bucketlist, BucketlistItem, UserProfile


class LoginRequiredMixin(object):
    """Enforces authentication before handling request"""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class RootView(View):
    """Handles request to the website root"""
    template_name = "website/index.html"

    def get(self, request, *args, **kwargs):
        """Returns response for `GET` request to the website root"""
        if request.user.is_authenticated():
            return redirect(reverse('app.dashboard'))
        return render(request,
                      self.template_name,
                      {
                          'page_title': 'Home',
                      }
                      )


class RootFilesView(View):
    """Renders requests for `robots.txt` and `humans.txt`"""

    def get(self, request, *args, **kwargs):
        """Returns response for `GET` request to the website root"""
        filename = self.kwargs.get('filename')
        return render(
            request, filename,
            {'page_title': filename}, content_type="text/plain"
        )


class StaticView(View):
    """Renders request for static pages"""

    def get(self, request, *args, **kwargs):
        """Returns response for `GET` requests for static files"""
        page = self.kwargs.get('page')
        try:
            return render(request,
                          'website/{0}.html'.format(page),
                          {'page_title': page.title()})
        except TemplateDoesNotExist:
            raise Http404()


class LoginView(View):
    """Renders requests for authorization."""

    def post(self, request, *args, **kwargs):
        """Handles logic and Returns response for `POST`
        requests to `/login`"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                user_backend = authenticate(
                    username=user.username,
                    password=password,
                )
                if not user_backend:
                    raise User.DoesNotExist()
                login(request, user_backend)
                return redirect(reverse('app.dashboard'))
            else:
                raise User.DoesNotExist()
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            messages.error(request, 'Wrong username or password.')
            return redirect(reverse('app.index'))


class LogoutView(View):
    """Renders request to logout authenticated session"""

    def get(self, request, *args, **kwargs):
        """Returns response for `GET` request to `/logout`"""
        logout(request)
        return redirect(reverse('app.index'))


class SignUpView(View):
    """Processes request to sign up a user"""

    def post(self, request, *args, **kwargs):
        """Handles logic and returns response for `POST`
        request to `/signup`"""
        if request.user.is_authenticated():
            return redirect(reverse('app.dashboard'))
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
        except ValueError:
            messages.error(request, 'Username must be set.')
            return redirect(reverse('app.index'))

        if user:
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request,
                'Hello {}, please kindly update \
                your profile information.'.format(first_name))
            return redirect(reverse('app.dashboard'))


class DashboardView(LoginRequiredMixin, View):
    """Renders dashboard for logged in user"""

    def get(self, request, *args, **kwargs):
        """Return response for `GET` requests to `/dashboard`"""
        return render(
            request,
            'website/dashboard.html',
            {
                'page_title': 'Bucketlists'
            }
        )


class BucketlistListView(LoginRequiredMixin, ListView):
    """Renders bucketlist for authenticated user"""
    model = Bucketlist
    template_name = 'website/bucketlist_list.html'
    paginate_by = 5

    def get_queryset(self, **kwargs):
        """Specifies a queryset to be rendered in the ListView"""
        query_string = self.request.GET.get('q', None)
        if query_string:
            return self.model.search(query_string)
        return self.model.objects.filter(
            user=self.request.user
        ).annotate(
            num_items=Count('bucketlistitem', distinct=True),
        )

    def get_context_data(self, **kwargs):
        """Specifies the context data to be returned in the response"""
        context = super(BucketlistListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', None)
        context['object'] = 'bucketlists'
        context['page_title'] = 'View Bucketlists'
        context['up_a_level'] = reverse('app.dashboard')
        return context


class BucketlistDetailView(LoginRequiredMixin, DetailView):

    """Renders bucketlist detail"""
    model = Bucketlist

    def get_context_data(self, **kwargs):
        """Specifies the context data to be returned in the response"""
        context = super(BucketlistDetailView, self).get_context_data(**kwargs)
        setattr(
            context['object'],
            'children',
            BucketlistItem.objects.filter(bucketlist=context['object'].id)
        )
        context['page_title'] = "View Bucketlist"
        context['up_a_level'] = reverse('app.bucketlists')
        return context


class BucketlistCreateView(LoginRequiredMixin, CreateView):
    """Handles creation of a bucketlist"""
    model = Bucketlist
    fields = ['name']

    def get_success_url(self, pk):
        """Specifies redirect URL if handling is processed successfully"""
        return reverse_lazy('app.bucketlist', kwargs={'pk': pk})

    def post(self, request):
        """ Overrides `POST` method to save bucketlist with user_id"""
        form_cls = self.get_form_class()
        form = form_cls(request.POST)
        form_model = form.save(commit=False)
        form_model.user_id = request.user.id
        form_model.save()
        return redirect(self.get_success_url(pk=form_model.id))


class BucketlistUpdateView(LoginRequiredMixin, UpdateView):
    """Handles update of a bucketlist"""
    model = Bucketlist
    fields = ['name']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('app.bucketlists')

    def get_context_data(self, **kwargs):
        """Specifies the context data returned in the response"""
        context = super(BucketlistUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Update Bucketlist'
        return context


class BucketlistDeleteView(LoginRequiredMixin, DeleteView):
    """Handles deletion of a bucketlist"""
    model = Bucketlist
    success_url = reverse_lazy('app.bucketlists')

    def get_context_data(self, **kwargs):
        """Specifies the context data returned in the response"""
        context = super(BucketlistDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = 'Delete Bucketlist'
        return context


class BucketlistItemListView(LoginRequiredMixin, ListView):

    """Renders bucketlist edit view"""
    pass


class BucketlistItemCreateView(LoginRequiredMixin, CreateView):
    """Handles the creation of a bucketlist item"""
    model = BucketlistItem
    fields = ['name', 'done']

    def get_success_url(self, pk):
        """Specifies the redirect URL is processed handled successfully"""
        return reverse_lazy('app.bucketlist', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        """Specifies the context data returned in the response"""
        context = super(
            BucketlistItemCreateView, self).get_context_data(**kwargs)
        bucketlist = get_object_or_404(Bucketlist, pk=self.kwargs.get('pk'))
        context['object_name'] = bucketlist.name
        context['page_title'] = 'Create Bucketlist Item'
        return context

    def post(self, request, pk):
        """Overwrite post method to save bucketlist with user_id"""
        form_cls = self.get_form_class()
        form = form_cls(request.POST)
        form_model = form.save(commit=False)
        form_model.user_id = request.user.id
        bucketlist = get_object_or_404(Bucketlist, pk=pk)
        form_model.bucketlist = bucketlist
        form_model.save()
        return redirect(self.get_success_url(pk=bucketlist.id))


class BucketlistItemUpdateView(LoginRequiredMixin, UpdateView):
    """Handles the update of a bucketlist item"""
    model = BucketlistItem
    template_name_suffix = '_update_form'
    fields = ['name', 'done']

    def get_success_url(self, **kwargs):
        """Specifies the redirect URL is handling is successful"""
        id, item_id = self.kwargs.values()
        return reverse_lazy('app.bucketlist',
                            kwargs={'pk': id})

    def get_queryset(self, **kwargs):
        """Specifies the queryset used for the logic"""
        pk = self.kwargs.get('pk_item', None)
        return self.model.objects.get(pk=pk)

    def get_object(self, queryset=None, **kwargs):
        """Specifies the object that is updated"""
        if queryset is None:
            queryset = self.get_queryset(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        """Specifies the context data returned in the response"""
        context = super(
            BucketlistItemUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Update Bucketlist Item'
        return context


class BucketlistItemDeleteView(LoginRequiredMixin, DeleteView):
    """Renders bucketlist item delete confirmation"""
    model = BucketlistItem
    template_name_suffix = '_confirm_delete'

    def get_success_url(self, **kwargs):
        """Specifies the redirect URL if handling is successful"""
        id, item_id = self.kwargs.values()
        return reverse_lazy('app.bucketlist',
                            kwargs={'pk': id})

    def get_queryset(self, **kwargs):
        """Specifies the queryset used for the logic"""
        pk = self.kwargs.get('pk_item', None)
        return self.model.objects.get(pk=pk)

    def get_object(self, queryset=None, **kwargs):
        """Specifies the object that is deleted"""
        if queryset is None:
            queryset = self.get_queryset(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        """Specifies the context data returned in the response"""
        context = super(
            BucketlistItemDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = 'Delete Bucketlist Item'
        return context


class BucketlistItemDetailView(LoginRequiredMixin, DetailView):
    """Renders bucketlist item detail view"""
    model = BucketlistItem

    def get_queryset(self, **kwargs):
        """Specifies the queryset used for the logic"""
        pk = self.kwargs.get('pk_item', None)
        return self.model.objects.get(pk=pk)

    def get_object(self, queryset=None, **kwargs):
        """Specifies the object that is viewed"""
        if queryset is None:
            queryset = self.get_queryset(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        """Specifies the context data returned in the response"""
        item_id = self.kwargs.get('pk_item')
        context = {}
        context['object'] = get_object_or_404(BucketlistItem, pk=item_id)
        context['page_title'] = 'View Bucketlist Item'
        return context


class BucketlistItemDoneView(View):
    """Sets a bucketlist item done field to True"""

    def get(self, request, **kwargs):
        """Handles logic for setting a bucketlist item as done"""
        item_id = self.kwargs.get('pk_item')
        id = self.kwargs.get('pk')
        bucketlistitem = get_object_or_404(BucketlistItem, pk=item_id)
        bucketlistitem.done = True
        bucketlistitem.save()
        messages.success(request, "Bucketlist item was marked as done")
        return redirect(reverse('app.bucketlist', kwargs={'pk': id}))


class UserProfileView(LoginRequiredMixin, View):
    """Renders user profile page"""

    def get(self, request, *args, **kwargs):
        """Handles logic to retrieve user profile information"""
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user)

        return render(
            self.request,
            'website/profile.html',
            {'profile': profile,
             'page_title': 'Update Profile'
             })


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Renders user profile form and updates profile data on form submission"""
    model = UserProfile
    template_name_suffix = '_update_form'
    fields = ['age', 'bio']

    def get_success_url(self, **kwargs):
        """Specifies redirect URL if handling is successful"""
        return reverse_lazy('app.user_profile',)

    def get_object(self, queryset=None, **kwargs):
        """Specifies the object that is updated"""
        return self.model.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        """Specifies the context_data returned in the response"""
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Update Profile'
        return context
