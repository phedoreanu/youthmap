import datetime

from cities_light.models import Country, City
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from djangoratings.fields import RatingField


class About(models.Model):
    about = models.TextField()
    contact_name = models.TextField(blank=True)
    contact_title = models.CharField(max_length=80, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=80, blank=True)

class Activity(models.Model):
    name = models.CharField(max_length=80)
    icon = models.CharField(max_length=80, default='')
    svg_icon = models.CharField(max_length=10, default='')
    order = models.IntegerField(default=0)
    tooltip = models.CharField(max_length=80, default='')

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Activities'

    def __unicode__(self):
        return u'%s' % self.name


class Tag(models.Model):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return u'%s' % self.name


class Language(models.Model):
    PROFICIENCY = (
        (1, 'Beginner'),
        (2, 'Medium'),
        (3, 'Advanced'),
    )
    name = models.CharField(max_length=20)
    proficiency = models.IntegerField(max_length=1, choices=PROFICIENCY, default=1)


class Article(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='article', blank=True, null=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, help_text='Select some tags...')
    active = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True, default=now())

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u'%s' % self.title


class Newsletter(models.Model):
    email = models.EmailField()
    active = models.BooleanField()
    last_sent_date = models.DateField(null=True)

    def __unicode__(self):
        return u'%s' % self.email


class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='following_set')
    to_user = models.ForeignKey(User, related_name='followers_set')


class Profile(models.Model):
    AVAILABILITY = (
        (1, 'Full-time'),
        (2, 'Part-time'),
        (3, 'Freelance'),
        (4, 'Volunteering'),
    )
    PRIVACY = (
        (1, 'Anyone'),
        (2, 'Youthmap'),
        (3, 'Me'),
    )
    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
    )
    owner = models.OneToOneField(User, editable=False)
    title = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    interests = models.CharField(max_length=200, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    future_plans = models.TextField(null=True, blank=True)
    field_of_activity = models.ManyToManyField(Activity, null=True, blank=True,
                                               help_text='Choose your activity in which you are most experienced!')
    photo = models.ImageField(upload_to='profile', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    city = models.ForeignKey(City)
    country = models.ForeignKey(Country)
    availability = models.IntegerField(max_length=1, choices=AVAILABILITY, default=1)
    privacy = models.IntegerField(max_length=1, choices=PRIVACY, default=1, verbose_name='privacy settings')
    gender = models.IntegerField(max_length=1, choices=GENDER, default=1)
    views = models.BigIntegerField(default=0, editable=False)
    pub_date = models.DateTimeField(auto_now_add=True, default=now())
    tags = models.ManyToManyField(Tag, help_text='Select some tags...')
    other_field_of_activity = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.owner.get_full_name()

    def class_name(self):
        return u'%s' % self.__class__.__name__

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


class Organisation(models.Model):
    LOC = 'LOC'
    NAT = 'NAT'
    INT = 'INT'
    LEVEL_CHOICES = (
        (LOC, 'Local'),
        (NAT, 'National'),
        (INT, 'International'),
    )
    user = models.OneToOneField(User, editable=False, null=True)
    title = models.CharField(max_length=200, verbose_name="Organization's name")
    photo = models.ImageField(upload_to='organisation', blank=True, verbose_name='Logo')
    field_of_activity = models.ManyToManyField(Activity,
                                               help_text='Choose your activity in which you are most experienced!')
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name='year of foundation')
    website = models.URLField(blank=True, null=True)
    values = models.TextField(blank=True, null=True)
    mission = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    target_group = models.TextField(blank=True, null=True)
    activities = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    partners = models.TextField(blank=True, null=True,
                                help_text='Mention the partners you need and what are their roles')
    level_of_activity = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=LOC, blank=True)
    number_of_members = models.PositiveIntegerField(default=0, blank=True)
    contact_person_name = models.CharField(max_length=150, null=True, verbose_name="contact person's name", blank=True)
    official_position = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=30, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='owner_set', editable=False)
    pub_date = models.DateTimeField(auto_now_add=True, default=now())
    views = models.BigIntegerField(default=0, editable=False)
    tags = models.ManyToManyField(Tag, help_text='Select some tags...')
    other_field_of_activity = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return u'%s' % self.title

    def class_name(self):
        return u'%s' % self.__class__.__name__

    def get_absolute_url(self):
        return reverse('organisation', kwargs={'pk': self.pk})


class Experience(models.Model):
    name_of_institution = models.CharField(max_length=100, verbose_name='Name of the company')
    position = models.CharField(max_length=100)
    field_of_activity = models.ForeignKey(Activity, null=True)
    country = models.ForeignKey(Country, null=True)
    city = models.ForeignKey(City, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    website = models.URLField(blank=True, null=True, verbose_name='Company website')
    profile = models.ForeignKey(Profile, null=True, editable=False)

    def __unicode__(self):
        return u'%s' % self.name_of_institution

    def get_absolute_url(self):
        return reverse('profile_complete')

    @models.permalink
    def get_update_url(self):
        return 'experience_update', [str(self.pk)]

    @models.permalink
    def get_delete_url(self):
        return 'experience_delete', [str(self.pk)]


class Diploma(models.Model):
    type = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.type


class Speciality(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Specialities'
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name


class Education(models.Model):
    institution_name = models.CharField(max_length=100)
    diploma = models.OneToOneField(Diploma)
    speciality = models.OneToOneField(Speciality)
    country = models.ForeignKey(Country, null=True)
    city = models.ForeignKey(City, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    qualifications = models.TextField()
    skills = models.TextField(verbose_name='Skills and competences you developed')
    courses = models.TextField(verbose_name='What courses helped you in your current activity')
    official_website = models.URLField(blank=True, null=True)
    profile = models.ForeignKey(Profile, null=True)

    def __unicode__(self):
        return u'%s' % self.institution_name

    def get_absolute_url(self):
        return reverse('profile_complete')

    @models.permalink
    def get_update_url(self):
        return 'education_update', [str(self.pk)]

    @models.permalink
    def get_delete_url(self):
        return 'education_delete', [str(self.pk)]


class CommonInfo(models.Model):
    VISIBILITY = (
        (1, 'Public'),
        (2, 'Private')
    )
    title = models.CharField(max_length=100, help_text='Give a title to it')
    field_of_activity = models.ManyToManyField(Activity,
                                               help_text='Choose your activity in which you are most experienced!')
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    problem_addressed = models.TextField(null=True, blank=True,
                                         help_text='What is the main problem/need you targeted and why')
    slogan = models.TextField(null=True, blank=True,
                              help_text='Short sentence containing essential message for the public')
    description = models.TextField(help_text='Describe your activity so others can understand what you want to do')
    objectives = models.TextField(null=True, blank=True,
                                  help_text='Preferably SMART - Specific, Measurable, Achievable, Realistic, Time limited')
    milestones = models.TextField(null=True, blank=True, verbose_name='Steps',
                                  help_text='Shortly present the stages for achieving the goals')
    other_needs = models.TextField(blank=True)
    resources = models.ManyToManyField('MetaResource')
    resources_needed = models.ManyToManyField('MetaResource', related_name='%(app_label)s_%(class)s_needed')
    budget = models.IntegerField(null=True, blank=True, help_text='Show it in EUR')
    attachment = models.FileField(upload_to='idea', blank=True, null=True,
                                  help_text='Upload any relevant video/audio/document')
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(auto_now_add=True)
    visibility = models.IntegerField(max_length=1, choices=VISIBILITY, default=1)
    owner = models.ForeignKey(User)
    rating = RatingField(range=5)

    class Meta:
        abstract = True

    def class_name(self):
        return u'%s' % self.__class__.__name__


class Idea(CommonInfo):
    background = models.TextField(null=True, blank=True, verbose_name='Possible partners',
                                  help_text='Shortly present the context or situation')

    def get_absolute_url(self):
        return reverse('idea', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u'%s' % self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Project(CommonInfo):
    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})


class MetaResource(models.Model):
    title = models.CharField(max_length=80, verbose_name='name', help_text='Give a title to it')
    link = models.URLField(blank=True, null=True, verbose_name='website')
    owner = models.ForeignKey(User, default=1, editable=False)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, help_text='Select some tags...', blank=True)

    def class_name(self):
        return u'%s' % self.__class__.__name__

    def __unicode__(self):
        return u'%s' % self.title


class Event(MetaResource):
    field_of_activity = models.ManyToManyField(Activity,
                                               help_text='Choose your activity in which you are most experienced!')
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    guests = models.TextField(blank=True, null=True)
    participants = models.TextField(blank=True, null=True)
    partners = models.TextField(blank=True, null=True,
                                help_text='Mention the partners you need and what are their roles')
    program = models.TextField(blank=True, null=True, verbose_name='Program description')
    result = models.TextField(blank=True, verbose_name=' Results/impact of the event')
    attachment = models.FileField(upload_to='event', blank=True, help_text='Upload any relevant video/audio/document')
    pub_date = models.DateTimeField(auto_now_add=True, default=now())

    def get_absolute_url(self):
        return reverse('event', kwargs={'pk': self.pk})


class MediaResource(MetaResource):
    similar = models.TextField(verbose_name='This resource is similar to (what other resources?)', blank=True,
                               null=True)
    partners = models.TextField(verbose_name='Partners (who else is involved?)', blank=True,
                                null=True, help_text='Mention the partners you need and what are their roles')
    pub_date = models.DateTimeField(auto_now_add=True, default=now())
    attachment = models.FileField(upload_to='newmedia', blank=True, null=True,
                                  help_text='Upload any relevant video/audio/document')

    def get_absolute_url(self):
        #return reverse('media_resource', kwargs={'pk': self.pk})
        return reverse('media')