from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import DetailView, ListView, TemplateView

from youth.views import *
from youth.models import Idea, Project, Organisation, Event, MediaResource
from youthmap import settings


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'youth.views.index', name='index'),
                       url(r'^teaser/$', TeaserView.as_view(template_name='youth/teaser.html'), name='teaser'),

                       url(r'^thank-you/$', TemplateView.as_view(template_name='youth/thank_you.html'),
                           name='thank_you'),

                       url(r'^home/$', 'youth.views.home', name='home'),
                       url(r'^countries/$', 'youth.views.get_countries', name='get_countries'),
                       url(r'^diplomas/$', 'youth.views.get_diplomas', name='get_diplomas'),
                       url(r'^specialties/$', 'youth.views.get_specialties', name='get_specialties'),
                       url(r'^cities/(?P<pk>\d+)$', 'youth.views.get_cities', name='get_cities'),
                       url(r'^activities/$', 'youth.views.get_activities', name='get_activities'),
                       #url(r'^user/create/$', 'youth.views.create', name='create'),
                       url(r'^register/ajax/$', 'youth.views.register_ajax', name='register_ajax'),
                       url(r'^add_experience/$', 'youth.views.add_experience', name='add_experience'),
                       url(r'^add_add_education/$', 'youth.views.add_education', name='add_education'),
                       url(r'^newsletter/$', 'youth.views.register_newsletter', name='newsletter_ajax'),

                       url(r'^follow/$', 'youth.views.follow', name='follow'),
                       url(r'^unfollow/$', 'youth.views.unfollow', name='unfollow'),

                       url(r'^dashboard/$', 'youth.views.dashboard', name='dashboard'),

                       url(r'^resources/$', 'youth.views.resources', name='resources'),

                       url(r'^resources/organisations/$',
                           ListView.as_view(paginate_by=10, template_name='youth/organisations.html',
                                            model=Organisation),
                           name='organisations'),

                       url(r'^resources/members/$',
                           ListView.as_view(paginate_by=10, template_name='youth/members.html',
                                            queryset=Profile.objects.filter(owner__is_superuser=False,
                                                                            owner__is_active=1)),
                           name='member_list'),

                       # pk = parameter
                       url(r'^resources/members/(?P<pk>\d+)/$', ProfileDetailView.as_view(), name='profile'),
                       # pk = request.user
                       # same name for display redirect ;)
                       url(r'^profile/$', 'youth.views.profile', name='profile'),

                       url(r'^profile/edit/$', BasicProfileUpdateView.as_view(), name='profile_edit'),
                       url(r'^profile/complete/$', CompleteProfileUpdateView.as_view(), name='profile_complete'),

                       url(r'^organisation/(?P<pk>\d+)/$', OrganisationDetailView.as_view(), name='organisation'),
                       url(r'^organisation/add/$', OrganisationCreatePreview.as_view(), name='organisation_add'),
                       url(r'^organisation/(?P<pk>\d+)/update$', OrganisationUpdate.as_view(),
                           name='organisation_update'),
                       url(r'^organisation/(?P<pk>\d+)/delete$', OrganisationDelete.as_view(),
                           name='organisation_delete'),

                       url(r'^favorites$', 'youth.views.my_favorites', name='my_favorites'),

                       url(r'^connections/following/$', 'youth.views.my_connections_following',
                           name='my_connections_following'),
                       url(r'^connections/followers/$', 'youth.views.my_connections_followers',
                           name='my_connections_followers'),

                       url(r'^invite/$', 'youth.views.invite_fb', name='invite_fb'),
                       url(r'^invite/twitter/$', 'youth.views.invite_tw', name='invite_tw'),
                       url(r'^invite/and/promote/$', 'youth.views.invite_email', name='invite_email'),

                       url(r'^account/$', AccountSettingsViews.as_view(), name='account_settings'),
                       url(r'^change/email/$', 'youth.views.change_email', name='change_email'),
                       url(r'^change/password/$', 'youth.views.change_password', name='change_password'),

                       url(r'^account/notifications/$', 'youth.views.account_notifications',
                           name='account_notifications'),
                       url(r'^account/privacy/$', 'youth.views.account_privacy', name='account_privacy'),

                       url(r'^search/$', 'youth.views.search', name='search'),

                       url(r'^help/$', 'youth.views.help_me', name='help_me'),
                       url(r'^about/$', 'youth.views.about', name='about'),
                       url(r'^contact/$', 'youth.views.contact', name='contact'),
                       url(r'^terms/$', 'youth.views.terms', name='terms'),
                       url(r'^privacy/$', 'youth.views.privacy', name='privacy'),

                       url(r'^events/calendar/$', CalendarEventListView.as_view(), name='calendar'),
                       url(r'^calendar/$',
                           CalendarEventListView.as_view(template_name='youth/youthmap_calendar.html'),
                           name='youthmap_calendar'),

                       url(r'^resources/events/$',
                           ListView.as_view(paginate_by=10, template_name='youth/events.html', model=Event),
                           name='events'),
                       url(r'^resources/media/$',
                           ListView.as_view(paginate_by=10, template_name='youth/media.html', model=MediaResource),
                           name='media'),

                       url(r'^display/(?P<content_type>\w+)/(?P<pk>\d+)/$', 'youth.views.display', name='display'),

                       url(r'^article/(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='article'),

                       url(r'^idea/(?P<pk>\d+)/$', DetailView.as_view(model=Idea), name='idea'),
                       url(r'^ideas/$', ListViewWithArticleList.as_view(model=Idea, paginate_by=10), name='idea_list'),
                       url(r'^idea/add/$', IdeaCreatePreview.as_view(), name='idea_add'),
                       url(r'^idea/(?P<pk>\d+)/update/$', IdeaUpdate.as_view(), name='idea_update'),
                       url(r'^idea/(?P<pk>\d+)/delete/$', IdeaDelete.as_view(), name='idea_delete'),

                       url(r'^project/(?P<pk>\d+)/$', DetailView.as_view(model=Project), name='project'),
                       url(r'^projects/$', ListViewWithArticleList.as_view(model=Project, paginate_by=10),
                           name='project_list'),
                       url(r'^project/add/$', ProjectCreatePreview.as_view(), name='project_add'),
                       url(r'^project/(?P<pk>\d+)/update/$', ProjectUpdate.as_view(), name='project_update'),
                       url(r'^project/(?P<pk>\d+)/delete/$', ProjectDelete.as_view(), name='project_delete'),

                       url(r'^event/(?P<pk>\d+)/$', DetailView.as_view(model=Event), name='event'),
                       url(r'^event/add/$', EventCreateView.as_view(), name='event_add'),
                       url(r'^event/(?P<pk>\d+)/update/$', EventUpdate.as_view(), name='event_update'),
                       url(r'^event/(?P<pk>\d+)/delete/$', EventDelete.as_view(), name='event_delete'),

                       url(r'^mediaresource/(?P<pk>\d+)/$', DetailView.as_view(model=MediaResource),
                           name='mediaresource'),
                       url(r'^mediaresource/add/$', MediaResourceCreateView.as_view(), name='media_resource_add'),
                       url(r'^mediaresource/(?P<pk>\d+)/update/$', MediaResourceUpdate.as_view(),
                           name='media_resource_update'),
                       url(r'^mediaresource/(?P<pk>\d+)/delete/$', MediaResourceDelete.as_view(),
                           name='media_resource_delete'),

                       url(r'^experience/(?P<pk>\d+)/update/$', ExperienceUpdateView.as_view(),
                           name='experience_update'),
                       url(r'^experience/(?P<pk>\d+)/delete/$', ExperienceDeleteView.as_view(),
                           name='experience_delete'),

                       url(r'^education/(?P<pk>\d+)/update/$', EducationUpdateView.as_view(), name='education_update'),
                       url(r'^education/(?P<pk>\d+)/delete/$', EducationDeleteView.as_view(), name='education_delete'),

                       url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', name='jsi18n'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'youth/login.html'},
                           name='login'),
                       url(r'^login_ajax/$', 'youth.views.login_ajax', name='login_ajax'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'youth/index.html',
                                                                              'next_page': 'index'}, name='logout'),
                       url(r'^deactivate/$', 'youth.views.deactivate', name='deactivate'),

                       url(r'^forgot/$', 'youth.views.forgot', name='forgot'),
                       url(r'^send_contact/$', 'youth.views.send_contact', name='send_contact'),

                       url(r'rate/$', 'youth.views.rate', name='rate'),
                       # url(r'^youthmap/', include('youth.urls', namespace='youth')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^select2/', include('django_select2.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^media\/(?P<path>.*)$', 'django.views.static.serve',
                                 {'document_root': settings.MEDIA_ROOT}))
    urlpatterns += staticfiles_urlpatterns()
