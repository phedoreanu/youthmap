# Create your views here.
from itertools import chain
import json
from operator import attrgetter
import re
from time import time

from cities_light.models import Country, City
from django.contrib.admin.models import LogEntry, DELETION, CHANGE, ADDITION
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views import generic
from django.views.generic.list import BaseListView
from djangoratings.views import AddRatingView
from templated_email import send_templated_mail

from youth.forms import RegisterForm, IdeaForm, ProjectForm, OrganisationForm, EventForm, MediaResourceForm, \
    BasicProfileForm, CompleteProfileForm, ExperienceForm, EducationForm, BasicOrganisationForm, ChangeEmailForm, \
    YouthMapPasswordChangeForm, CompleteOrganisationForm
from youth.models import Idea, Project, Organisation, Event, MediaResource, Activity, Profile, Newsletter, Experience, \
    Education, Diploma, Speciality, Relationship, Article, About
from youthmap import settings


class CreatePreview(generic.CreateView):
    preview_template = None
    template_name = 'youth/idea_form.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST, request.FILES)
        form._user = request.user
        #if self.preview_template:
        #form.helper.add_input(YouthmapStrictButton('preview', css_class='medium dark'))

        if request.POST.get('country'):
            form.fields['city'].queryset = City.objects.filter(country=request.POST['country'])

        if form.is_valid():
            if 'preview' in request.POST:
                return render(request, self.preview_template, {'form': form})
            if 'edit' in request.POST:
                return render(request, self.template_name, {'form': form})

            youthmap_object = form.save()
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(youthmap_object).pk,
                object_id=youthmap_object.pk,
                object_repr=force_text(youthmap_object),
                action_flag=ADDITION,
            )
            return redirect(youthmap_object)
        return render(request, self.template_name, {'form': form})


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePreview, self).dispatch(*args, **kwargs)


class GenericUpdateView(generic.UpdateView):
    def get_form(self, form_class):
        form = super(GenericUpdateView, self).get_form(form_class)
        if hasattr(self.object, 'country'):
            form.fields['city'].queryset = City.objects.filter(country=self.object.country.pk).order_by('display_name')
        return form


class CommonUpdateView(GenericUpdateView):
    template_name = 'youth/idea_form.html'

    # restricting updates to owners
    def get_queryset(self):
        base_qs = super(CommonUpdateView, self).get_queryset()
        return base_qs.filter(owner=self.request.user)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form._user = request.user

        if request.POST.get('country'):
            form.fields['city'].queryset = City.objects.filter(country=request.POST['country'])

        if form.is_valid:
            youthmap_object = form.save()
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(youthmap_object).pk,
                object_id=youthmap_object.pk,
                object_repr=force_text(youthmap_object),
                action_flag=CHANGE,
                #change_message=youthmap_object.__class__.__name__.lower()
            )
            if self.success_url:
                return redirect(self.success_url)
            return redirect(youthmap_object)
        return render(request, self.template_name, {'form': form})


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommonUpdateView, self).dispatch(*args, **kwargs)


class GenericDetailView(generic.DetailView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenericDetailView, self).dispatch(*args, **kwargs)


class GenericDeleteView(generic.DeleteView):
    #restricting deletes to owners
    #def get_queryset(self):
    #    base_qs = super(GenericDeleteView, self).get_queryset()
    #    return base_qs.filter(owner=self.request.user)
    #
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenericDeleteView, self).dispatch(*args, **kwargs)


# Idea CRUD
class IdeaCreatePreview(CreatePreview):
    preview_template = 'youth/idea_preview.html'
    form_class = IdeaForm
    model = Idea


class IdeaUpdate(CommonUpdateView):
    form_class = IdeaForm
    model = Idea


class IdeaDelete(GenericDeleteView):
    model = Idea
    success_url = reverse_lazy('index')


# Project CRUD
class ProjectCreatePreview(CreatePreview):
    preview_template = 'youth/project_preview.html'
    form_class = ProjectForm
    model = Project


class ProjectUpdate(CommonUpdateView):
    model = Project
    form_class = ProjectForm


class ProjectDelete(GenericDeleteView):
    model = Project
    success_url = reverse_lazy('index')


# Organisation CRUD
class OrganisationCreatePreview(CreatePreview):
    template_name = 'youth/resource_add.html'
    preview_template = 'youth/organisation_preview.html'
    form_class = OrganisationForm


class OrganisationUpdate(CommonUpdateView):
    model = Organisation
    form_class = OrganisationForm


class OrganisationDelete(GenericDeleteView):
    model = Organisation
    success_url = reverse_lazy('index')


# Event CRUD
class EventCreateView(CreatePreview):
    template_name = 'youth/resource_add.html'
    preview_template = 'youth/event_preview.html'
    form_class = EventForm


class EventUpdate(CommonUpdateView):
    model = Event
    form_class = EventForm


class EventDelete(GenericDeleteView):
    model = Event
    success_url = reverse_lazy('index')


# MediaResource CRUD
class MediaResourceCreateView(CreatePreview):
    template_name = 'youth/resource_add.html'
    preview_template = 'youth/media_resource_preview.html'
    form_class = MediaResourceForm


class MediaResourceUpdate(CommonUpdateView):
    model = MediaResource
    form_class = MediaResourceForm


class MediaResourceDelete(GenericDeleteView):
    model = MediaResource
    success_url = reverse_lazy('index')


class ExperienceUpdateView(CommonUpdateView):
    model = Experience
    form_class = ExperienceForm


class ExperienceDeleteView(GenericDeleteView):
    model = Experience
    success_url = reverse_lazy('profile_complete')


class EducationUpdateView(CommonUpdateView):
    model = Education
    form_class = EducationForm


class EducationDeleteView(GenericDeleteView):
    model = Education
    success_url = reverse_lazy('profile_complete')


def index(request):
    if request.user.is_authenticated():
        return redirect('home')
    return render(request, 'youth/index.html')
    # return render(request, 'youth/teaser.html')


def home(request):
    logs = LogEntry.objects.exclude(action_flag=DELETION).exclude(user__is_superuser=True).exclude(
        user__is_active=False).order_by('-action_time')[:30]

    latest_resources = sorted(
        chain(
            Idea.objects.filter(owner__is_active=True).order_by('-pub_date')[:15],
            Project.objects.filter(owner__is_active=True).order_by('-pub_date')[:15],
            Event.objects.filter(owner__is_active=True).order_by('-pub_date')[:15],
            Organisation.objects.filter(owner__is_active=True).order_by('-pub_date')[:15]),
        key=attrgetter('pub_date'), reverse=True)

    ideas_map = Idea.objects.order_by('-pub_date')[:200].all()

    article_list = Article.objects.filter(active=True).order_by('-pub_date')[:7]

    return render(request, 'youth/home.html',
                  {'ideas': Idea.objects.filter(owner__is_active=True).order_by('-pub_date')[:20],
                   'projects': Project.objects.filter(owner__is_active=True).order_by('-pub_date')[:20],
                   'resources': latest_resources, 'logs': logs,
                   'ideas_map': ideas_map,
                   'article_list': article_list,
                  })


class PaginatedResourcesView(BaseListView):
    pass


def resources(request):
    latest_resources = sorted(
        chain(
            Idea.objects.filter(owner__is_active=True).order_by('-pub_date')[:15],
            Project.objects.filter(owner__is_active=True).order_by('-pub_date')[:15],
            Event.objects.filter(owner__is_active=True).order_by('-pub_date')[:15],
            Organisation.objects.filter(owner__is_active=True).order_by('-pub_date')[:15]),
        key=attrgetter('pub_date'), reverse=True)

    return render(request, 'youth/resources.html', {'resources': latest_resources})


def organisations(request):
    return render(request, 'youth/organisations.html')


@login_required
def dashboard(request):
    return render(request, 'youth/dashboard.html')


def login_ajax(request):
    if request.method == 'POST':
        if request.POST.get('remember_me') == '1':
            # 2 weeks
            request.session.set_expiry(1209600)
        # else:
        #     request.session.set_expiry(0)
        username = request.POST['username']
        password = request.POST['password']
        redirect_to = request.POST['next']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({'message': 'ok', 'redirect': redirect_to.replace('logout', 'home')}),
                                    mimetype="application/json")
        return HttpResponse(json.dumps({'message': 'Your username or password are not correct.',
                                        'element_id': '.login-error-message'}), mimetype="application/json")
    else:
        return HttpResponseForbidden()


def register_ajax(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            redirect_to = request.POST['next']
            message = u'ok'

            try:
                int(form.cleaned_data['country'])
                int(form.cleaned_data['city'])
            except ValueError:
                message = u'Select your location!'

            try:
                int(form.cleaned_data['activity'])
            except ValueError:
                message = u'Select your field of activity!'

            if message == u'ok':
                u = User.objects.filter(username=form.cleaned_data['username'])
                if u:
                    message = u'Username already in use!'
                u1 = User.objects.filter(email=form.cleaned_data['email'])
                if u1:
                    message = u'Email address already in use!'
                if not u and not u1 and message == 'ok':
                    user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                    form.cleaned_data['password'])
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.save()

                    status = int(form.cleaned_data['status'])

                    if status == 1:
                        p = Profile(owner=user, title=form.cleaned_data['title'],
                                    city=City.objects.get(pk=form.cleaned_data['city']),
                                    country=Country.objects.get(pk=form.cleaned_data['country']),
                                    other_field_of_activity=form.cleaned_data['other'])
                        p.save()
                        p.field_of_activity.add(Activity.objects.get(id=form.cleaned_data['activity']))
                    else:
                        o = Organisation(user=user, owner=user, title=form.cleaned_data['title'],
                                         city=City.objects.get(pk=form.cleaned_data['city']),
                                         country=Country.objects.get(pk=form.cleaned_data['country']),
                                         other_field_of_activity=form.cleaned_data['other'],
                                         email=form.cleaned_data['email'])
                        o.save()
                        o.field_of_activity.add(Activity.objects.get(id=form.cleaned_data['activity']))

                    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                    login(request, user)

                    send_templated_mail(
                        template_name='welcome',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        context={
                            'username': user.username,
                            'full_name': user.get_full_name(),
                            'signup_date': user.date_joined
                        },
                        # Optional:
                        # cc=['cc@example.com'],
                        # bcc=['bcc@example.com'],
                        # headers={'My-Custom-Header':'Custom Value'},
                        # template_prefix="my_emails/",
                        # template_suffix="email",
                    )
            return HttpResponse(json.dumps({'message': message, 'redirect': redirect_to.replace('logout', 'home'),
                                            'element_id': '#register-error-message'}), mimetype="application/json")
        else:
            return HttpResponse(json.dumps({'message': 'form invalid!'}), mimetype="application/json")
    else:
        return HttpResponseForbidden()


def register_newsletter(request):
    if request.method == "POST" and request.POST.get('newsletter'):
        from django.core.exceptions import ValidationError
        from django.core.validators import validate_email

        try:
            validate_email(request.POST['newsletter'])
            Newsletter(email=request.POST['newsletter'], active=True).save()
            return HttpResponse(json.dumps({'message': 'ok'}), mimetype="application/json")
        except ValidationError:
            return HttpResponse(json.dumps({'message': 'nok'}), mimetype="application/json")
    else:
        return HttpResponseForbidden()


def get_countries(request):
    data = serializers.serialize('json', Country.objects.all().order_by('name'), fields=('pk', 'name'))
    return HttpResponse(data, mimetype="application/json")


def get_cities(request, pk):
    data = serializers.serialize('json', City.objects.filter(country=pk).order_by('name'), fields=('pk', 'name'))
    return HttpResponse(data, mimetype="application/json")


def get_activities(request):
    data = serializers.serialize('json', Activity.objects.all())
    return HttpResponse(data, mimetype="application/json")


# TEMP!
@login_required
def get_diplomas(request):
    data = serializers.serialize('json', Diploma.objects.all())
    return HttpResponse(data, mimetype="application/json")


# TEMP!
@login_required
def get_specialties(request):
    data = serializers.serialize('json', Speciality.objects.all())
    return HttpResponse(data, mimetype="application/json")


class TeaserView(generic.FormView):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            User.objects.get(username=request.POST['username'])
            username = request.POST['username'] + u'_' + time().__str__()
        except User.DoesNotExist:
            username = request.POST['username']

        user = User.objects.create_user(username, request.POST['email'], username)
        p = Profile(owner=user, country=Country.objects.get(pk=request.POST['country']),
                    city=City.objects.get(pk=1))
        p.save()

        return HttpResponseRedirect(reverse('thank_you'))


class ProfileDetailView(GenericDetailView):
    model = Profile
    template_name = 'youth/member_detail.html'

    def get_object(self, queryset=None):
        p = super(ProfileDetailView, self).get_object(queryset)
        p.views += 1
        p.save()
        return p


class OrganisationDetailView(GenericDetailView):
    model = Organisation

    def get_object(self, queryset=None):
        o = super(OrganisationDetailView, self).get_object(queryset)
        o.views += 1
        o.save()
        return o


class ArticleDetailView(GenericDetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context_data = super(ArticleDetailView, self).get_context_data(**kwargs)
        context_data['article_list'] = Article.objects.filter(active=True).order_by('-pub_date')[:20]
        return context_data


class ListViewWithArticleList(generic.ListView):
    def get_context_data(self, **kwargs):
        context_data = super(ListViewWithArticleList, self).get_context_data(**kwargs)
        context_data['article_list'] = Article.objects.filter(active=True).order_by('-pub_date')[:20]
        return context_data


class CalendarEventListView(generic.ListView):
    template_name = 'youth/calendar.html'
    model = Event


def display(request, content_type, pk):
    return redirect('%s' % content_type, pk=pk)


@login_required
def profile(request):
    try:
        p = Profile.objects.get(pk=request.user.profile.id)
    except Profile.DoesNotExist:
        p = Organisation.objects.get(pk=request.user.organisation.id)

    logs = LogEntry.objects.exclude(action_flag=DELETION).filter(user=request.user).order_by('-action_time')[:7]

    return render(request, 'youth/profile.html', {'profile': p, 'logs': logs})


class BasicProfileUpdateView(generic.TemplateView):
    template_name = 'youth/profile_edit.html'

    def get(self, request, *args, **kwargs):
        try:
            p = Profile.objects.get(pk=request.user.profile.id)
            form = BasicProfileForm(initial={'first_name': p.owner.first_name, 'last_name': p.owner.last_name},
                                    instance=p)
        except Profile.DoesNotExist:
            p = Organisation.objects.get(pk=request.user.organisation.id)
            self.template_name = 'youth/organisation_profile_edit.html'
            form = BasicOrganisationForm(initial={'first_name': p.owner.first_name, 'last_name': p.owner.last_name},
                                         instance=p)
        if form.fields.get('country'):
            # order by name
            form.fields['country'].queryset = Country.objects.all().order_by('name')
            # filter by country
            form.fields['city'].queryset = City.objects.filter(country=p.country.pk).order_by('display_name')
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            p = Profile.objects.get(pk=request.user.profile.id)
            form = BasicProfileForm(request.POST, request.FILES, instance=p)
            is_profile = True
        except Profile.DoesNotExist:
            p = Organisation.objects.get(pk=request.user.organisation.id)
            form = BasicOrganisationForm(request.POST, request.FILES, instance=p)
            self.template_name = 'youth/organisation_profile_edit.html'
            is_profile = False

        if request.POST.get('country'):
            # filter by country
            form.fields.get('city').queryset = City.objects.filter(country=request.POST.get('country')).order_by(
                'display_name')

        if form.is_valid():
            if is_profile:
                p.owner.first_name = form.cleaned_data['first_name']
                p.owner.last_name = form.cleaned_data['last_name']
                p.owner.save(update_fields=['first_name', 'last_name'])

            #LogEntry.objects.log_action(
            #    user_id=request.user.pk,
            #    content_type_id=ContentType.objects.get_for_model(p).pk,
            #    object_id=p.pk,
            #    object_repr=force_text(p),
            #    action_flag=CHANGE,
            #    change_message='the profile'
            #)
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BasicProfileUpdateView, self).dispatch(*args, **kwargs)


class CompleteProfileUpdateView(generic.FormView):
    template_name = 'youth/profile_complete.html'

    def get(self, request, *args, **kwargs):
        try:
            p = Profile.objects.get(pk=request.user.profile.id)
            form = CompleteProfileForm(instance=p)
        except Profile.DoesNotExist:
            p = Organisation.objects.get(pk=request.user.organisation.id)
            self.template_name = 'youth/organisation_profile_complete.html'
            form = CompleteOrganisationForm(instance=p)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            p = Profile.objects.get(pk=request.user.profile.id)
            form = CompleteProfileForm(request.POST, instance=p)
        except Profile.DoesNotExist:
            p = Organisation.objects.get(pk=request.user.organisation.id)
            form = CompleteOrganisationForm(request.POST, instance=p)
            self.template_name = 'youth/organisation_profile_complete.html'
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CompleteProfileUpdateView, self).dispatch(*args, **kwargs)


# TEMP!
@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)

        #if form.fields.get('country'):
        #    # filter by country
        #    form.fields.get('city').queryset = City.objects.filter(country=request.POST.get('country')).order_by(
        #        'display_name')

        if form.is_valid():
            e = form.save()
            request.user.profile.experience_set.add(e)

        return HttpResponse(json.dumps({'message': 'ok', 'redirect': request.POST['next']}),
                            mimetype="application/json")
    else:
        return HttpResponseForbidden()


# TEMP!
@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            e = form.save()
            request.user.profile.education_set.add(e)

        return HttpResponse(json.dumps({'message': 'ok', 'redirect': request.POST['next']}),
                            mimetype="application/json")
    else:
        return HttpResponseForbidden()


@login_required
def my_favorites(request):
    return render(request, 'youth/my_favorites.html')


@login_required
def follow(request):
    if request.method == "POST":
        to_user = User.objects.get(pk=request.POST['follower-id'])
        r, created = Relationship.objects.get_or_create(from_user=request.user, to_user=to_user)
        message = 'Unfollow'
        if not created:
            r.delete()
            message = 'Follow'
        return HttpResponse(json.dumps({'message': message}), mimetype="application/json")
    else:
        return HttpResponseForbidden()


@login_required
def unfollow(request):
    if request.method == "POST":
        Relationship.objects.get(from_user=request.user.id, to_user=request.POST['follower-id']).delete()
        return redirect('my_connections_following')
    else:
        return HttpResponseForbidden()


@login_required
def my_connections_following(request):
    user_list = [val.to_user_id for val in request.user.following_set.all()]
    following_profiles = chain(Profile.objects.filter(owner__in=user_list),
                               Organisation.objects.filter(user__in=user_list))
    return render(request, 'youth/my_connections_following.html', {'object_list': following_profiles})


@login_required
def my_connections_followers(request):
    user_list = [val.from_user_id for val in request.user.followers_set.all()]
    followed_profiles = chain(Profile.objects.filter(owner__in=user_list),
                              Organisation.objects.filter(user__in=user_list))
    return render(request, 'youth/my_connections_followers.html', {'object_list': followed_profiles})


@login_required
def invite_fb(request):
    return render(request, 'youth/invite_fb.html')


@login_required
def invite_tw(request):
    return render(request, 'youth/invite_tw.html')


@login_required
def invite_email(request):
    return render(request, 'youth/invite_email.html')


@login_required
def help_me(request):
    return render(request, 'youth/help_me.html')


class AccountSettingsViews(generic.TemplateView):
    template_name = 'youth/account_settings.html'

    def get(self, request, *args, **kwargs):
        email_form = ChangeEmailForm()
        password_form = YouthMapPasswordChangeForm(request.user)

        return render(request, self.template_name, {'email_form': email_form, 'password_form': password_form})


@login_required
def change_email(request):
    if request.method == 'POST':
        email_form = ChangeEmailForm(request.POST)
        if email_form.is_valid():
            email_form.save(request.user)
            #return render(request, 'youth/account_settings.html',
            #              {'email_success_message': u'Your email was updated successfully!'})
            return redirect('account_settings')

        password_form = YouthMapPasswordChangeForm(request.user)
        return render(request, 'youth/account_settings.html',
                      {'email_form': email_form, 'password_form': password_form})
    return redirect('account_settings')


@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = YouthMapPasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            return redirect('account_settings')
            #{'pass_success_message': 'Your password was updated successfully!'})

        email_form = ChangeEmailForm()
        return render(request, 'youth/account_settings.html',
                      {'email_form': email_form, 'password_form': password_form})
    return redirect('account_settings')


@login_required
def account_notifications(request):
    return render(request, 'youth/account_notifications.html')


@login_required
def account_privacy(request):
    return render(request, 'youth/account_privacy.html')


@login_required
def search(request):
    if request.method == 'POST':
        query_string = '%s %s' % (request.POST.get('q'), request.POST.get('w'))
        field_of_activity = request.POST.get('foa')
        result_list = get_search_results(query_string, field_of_activity, [Idea, Project, Organisation, Event, Profile])
        return render(request, 'youth/search.html', {'result_list': result_list, 'query_string': query_string})
    return redirect('home')


def get_search_results(query_string, field_of_activity=None, models=None):
    results = []
    if models:
        for model in models:
            query_set = model.objects.filter(owner__is_active=True)
            if query_string.strip():
                entry_query = get_query(query_string, ['title', 'city__search_names', 'tags__name'])
                query_set = query_set.filter(entry_query)
            if field_of_activity:
                query_set = query_set.filter(field_of_activity=field_of_activity)
            results.extend(query_set.order_by('-pub_date'))
    return results


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        #>>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def rate(request):
    if request.method == 'POST':
        rater = request.POST.get('id').split('_')
        params = {
            'content_type_id': ContentType.objects.get_for_model(eval(rater[0])).pk,
            'object_id': rater[1],
            'field_name': 'rating',
            'score': request.POST.get('rating'),  # the score value they're sending
        }
        response = AddRatingView()(request, **params)
        return HttpResponse(json.dumps({'message': response.content, 'rating': params['score']}),
                            mimetype="application/json")
    else:
        return HttpResponseForbidden()


def calendar(request):
    return render(request, 'youth/calendar.html')


# TEMP!
@login_required
def deactivate(request):
    if request.method == 'POST' and request.POST.get('agree'):
        u = User.objects.get(pk=request.user.id)
        u.is_active = False
        u.save()
        return redirect('logout')
    else:
        return HttpResponseForbidden()


def about(request):
    return render(request, 'youth/about.html', {'about': About.objects.get(pk=1)})


def contact(request):
    return render(request, 'youth/contact.html', {'about': About.objects.get(pk=1)})


def terms(request):
    return render(request, 'youth/terms.html')


def privacy(request):
    return render(request, 'youth/privacy.html')


def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            u = User.objects.get(email=email)
            password = User.objects.make_random_password()
            u.set_password(password)
            u.save()

            send_templated_mail(
                template_name='forgot',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                context={
                    'username': u.username,
                    'full_name': u.get_full_name(),
                    'password': password
                },
            )
        except User.DoesNotExist or User.MultipleObjectsReturned:
            return redirect('index')

        return redirect('home')


def send_contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        try:
            send_templated_mail(
                template_name='send_contact',
                from_email=email,
                recipient_list=[About.objects.get(pk=1).contact_email],
                context={
                    'full_name': full_name,
                    'message': message
                },
            )
        except User.DoesNotExist or User.MultipleObjectsReturned:
            return redirect('index')

        return redirect('home')