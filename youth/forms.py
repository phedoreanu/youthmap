# coding=utf-8
from cities_light.models import City, Country
from crispy_forms.bootstrap import StrictButton, FormActions
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm, widgets
from crispy_forms.utils import flatatt
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django_select2 import Select2MultipleWidget, AutoModelSelect2TagField, AutoHeavySelect2TagWidget
from suit.widgets import NumberInput
from youth.models import Idea, Project, Organisation, Event, MediaResource, Profile, Education, Experience, Tag, MetaResource

__author__ = 'fedo'
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div


class YouthmapStrictButton(StrictButton):
    field_classes = 'green button2 save marginSemiTop'

    def __init__(self, content, **kwargs):
        super(YouthmapStrictButton, self).__init__(content, **kwargs)
        self.content = content
        self.template = kwargs.pop('template', self.template)

        kwargs.setdefault('type', 'add')
        kwargs.setdefault('name', self.content)

        # We turn css_id and css_class into id and class
        if 'css_id' in kwargs:
            kwargs['id'] = kwargs.pop('css_id')
        kwargs['class'] = self.field_classes
        if 'css_class' in kwargs:
            kwargs['class'] += " %s" % kwargs.pop('css_class')

        self.flat_attrs = flatatt(kwargs)


class YouthmapSelect2MultipleWidget(Select2MultipleWidget):
    def init_options(self):
        super(YouthmapSelect2MultipleWidget, self).init_options()
        self.options['width'] = '100%'
        self.options['closeOnSelect'] = False
        #self.options['minimumInputLength'] = 1
        #self.options['maximumInputLength'] = 5
        self.options['minimumResultsForSearch'] = 10
        self.options['maximumSelectionSize'] = 3


class TagsHeavySelect2TagWidget(AutoHeavySelect2TagWidget):
    def init_options(self):
        super(TagsHeavySelect2TagWidget, self).init_options()
        self.options['width'] = '100%'
        self.options['closeOnSelect'] = False
        self.options['minimumInputLength'] = 1
        self.options['maximumInputLength'] = 30
        self.options['minimumResultsForSearch'] = 10
        self.options['maximumSelectionSize'] = 6


class TagChoices(AutoModelSelect2TagField):
    queryset = Tag.objects.all()
    search_fields = ['name__icontains']
    widget = TagsHeavySelect2TagWidget

    def get_model_field_values(self, value):
        return {'name': value}


class ResourcesChoices(AutoModelSelect2TagField):
    queryset = MetaResource.objects.all()
    search_fields = ['title__icontains']
    widget = TagsHeavySelect2TagWidget

    def get_model_field_values(self, value):
        return {'title': value}


class InlineRadioFieldRenderer(widgets.RadioFieldRenderer):
    def render(self):
        return mark_safe(u'\n%s\n' % u'\n'.join([u'%s' % force_unicode(w) for w in self]))


class InlineRadioSelect(widgets.RadioSelect):
    renderer = InlineRadioFieldRenderer


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    activity = forms.CharField(max_length=100)
    status = forms.ChoiceField(choices=((1, 'Ind'), (2, 'Org')))
    other = forms.CharField(max_length=100, required=False)


class BasicProfileForm(ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    tags = TagChoices(required=False)

    class Meta:
        model = Profile
        fields = ('title', 'date_of_birth', 'interests', 'website', 'city', 'country',
                  'photo', 'availability', 'gender', 'tags')
        widgets = {
            'availability': InlineRadioSelect(),
            'gender': InlineRadioSelect(),
        }


class CompleteProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('about_me', 'future_plans', 'field_of_activity', 'other_field_of_activity', 'privacy')
        widgets = {
            'field_of_activity': YouthmapSelect2MultipleWidget(),
            'privacy': InlineRadioSelect(),
        }


class BasicOrganisationForm(ModelForm):
    #first_name = forms.CharField(max_length=100)
    #last_name = forms.CharField(max_length=100)

    class Meta:
        model = Organisation
        fields = ('title', 'field_of_activity', 'other_field_of_activity', 'year', 'website', 'city', 'country',
                  'photo', 'values')
        widgets = {
            'field_of_activity': YouthmapSelect2MultipleWidget(),
        }


class CompleteOrganisationForm(ModelForm):
    tags = TagChoices(required=False)

    class Meta:
        model = Organisation
        fields = ('mission', 'objectives', 'target_group', 'achievements', 'partners', 'level_of_activity', 'tags',
                  'number_of_members', 'contact_person_name', 'official_position', 'email', 'telephone')


class YouthmapGenericModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(YouthmapGenericModelForm, self).__init__(*args, **kwargs)
        self.model_name = self._meta.model.__name__
        if self.model_name.startswith('Media'):
            self.model_name = 'Media Resource'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'

        if hasattr(self.fields, 'tags'):
            self.fields[
                'tags'].help_text = 'write individual tags which will help other users to locate your %s' % self.model_name

        # update
        if self.instance.pk:
            self.form_actions = FormActions(YouthmapStrictButton('save', css_class='medium green'))
        else:
        # insert
            self.form_actions = FormActions(
                YouthmapStrictButton('submit', css_class='medium green'),
                YouthmapStrictButton('preview', css_class='medium dark')
            )


class YouthmapGenericModelFormWithOwner(YouthmapGenericModelForm):
    def save(self, commit=True):
        inst = super(YouthmapGenericModelFormWithOwner, self).save(commit=False)
        inst.owner = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class ExperienceForm(YouthmapGenericModelForm):
    class Meta:
        model = Experience


class EducationForm(YouthmapGenericModelForm):
    class Meta:
        model = Education
        exclude = ['profile']


class YouthmapForm(YouthmapGenericModelFormWithOwner):
    country = forms.ModelChoiceField(queryset=Country.objects.order_by('name'), cache_choices=True)
    city = forms.ModelChoiceField(queryset=City.objects.none(), cache_choices=True)
    tags = TagChoices(required=False)

    def clean_end_date(self):
        cleaned_data = super(YouthmapForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('is before start date')
        return end_date

    class Meta:
        abstract = True
        exclude = ('owner',)
        widgets = {
            'field_of_activity': YouthmapSelect2MultipleWidget(),
            'budget': NumberInput(attrs={'class': 'input-mini'}),
            'year': NumberInput(attrs={'class': 'input-mini'}),
            'visibility': InlineRadioSelect(),
            'country': forms.Select(attrs={'class': 'left-column'}),
        }


class IdeaForm(YouthmapForm):
    resources = ResourcesChoices(required=False)
    resources_needed = ResourcesChoices(required=False)

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.fields['resources'].label = 'Resources we have'
        self.fields['resources'].help_text = 'Write what resources you already have'
        self.fields['resources_needed'].label = 'Resources we need'
        self.fields['resources_needed'].help_text = 'Write what you do not have and need'

        self.helper.layout = Layout(
            Field('title'),
            Field('field_of_activity'),
            Field('country', wrapper_class='left-column'),
            Field('city', wrapper_class='right-column'),
            Div(css_class='clearfix'),
            Field('start_date', wrapper_class='left-column'),
            Field('end_date', wrapper_class='right-column'),
            Field('budget', wrapper_class='left-column'),
            Div(css_class='clearfix'),
            Field('slogan'),
            Field('problem_addressed'),
            Field('description'),            
            Field('objectives'),
            Field('milestones'),
			Field('background'),
            Field('resources', wrapper_class='left-column', ),
            Field('resources_needed', wrapper_class='right-column'),
            Div(css_class='clearfix'),
            Field('other_needs'),
            Field('attachment'),
            Field('tags'),
            Field('visibility', template='youthmap/field.html'),
            self.form_actions
        )

    class Meta(YouthmapForm.Meta):
        model = Idea
        #exclude = ['visibility']


class ProjectForm(IdeaForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('title'),
            Field('field_of_activity'),
            Field('country', wrapper_class='left-column'),
            Field('city', wrapper_class='right-column'),
            Field('start_date', wrapper_class='left-column'),
            Field('end_date', wrapper_class='right-column'),
            Field('budget', wrapper_class='left-column'),
            Div(css_class='clearfix'),
            Field('slogan'),
            Field('problem_addressed'),
            Field('description'),
            Field('objectives'),
            Field('milestones'),
            Field('resources', wrapper_class='left-column'),
            Field('resources_needed', wrapper_class='right-column'),
            Div(css_class='clearfix'),
            Field('other_needs'),
            Field('attachment'),
            Field('tags'),
            Field('visibility', template='youthmap/field.html'),
            self.form_actions
        )

    class Meta(IdeaForm.Meta):
        model = Project


class OrganisationForm(YouthmapForm):
    class Meta(YouthmapForm.Meta):
        model = Organisation

    def __init__(self, *args, **kwargs):
        super(OrganisationForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('title'),
            Field('field_of_activity'),
            Field('country', wrapper_class='left-column'),
            Field('city', wrapper_class='right-column'),
            Field('year', wrapper_class='left-column'),
            Div(css_class='clearfix'),
            Field('photo'),
            Field('website'),
            Field('values'),
            Field('objectives'),
            Field('activities'),
            Field('achievements'),
            Field('partners'),
            Field('level_of_activity'),
            Field('number_of_members'),
            Field('contact_person_name'),
            Field('official_position'),
            Field('email'),
            Field('telephone'),
            Field('tags'),
            self.form_actions
        )


class EventForm(YouthmapForm):
    class Meta(YouthmapForm.Meta):
        model = Event

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('title'),
            Field('field_of_activity'),
            Field('country', wrapper_class='left-column'),
            Field('city', wrapper_class='right-column'),
            Field('start_date', wrapper_class='left-column'),
            Field('end_date', wrapper_class='right-column'),
            Div(css_class='clearfix'),
            #Field('website'),
            Field('link'),
            Field('description'),
            Field('guests'),
            Field('participants'),
            Field('partners'),
            Field('program'),
            Field('result'),
            Field('attachment'),
            Field('tags'),
            self.form_actions
        )


class MediaResourceForm(YouthmapGenericModelFormWithOwner):
    tags = TagChoices(required=False)

    class Meta(YouthmapForm.Meta):
        model = MediaResource

    def __init__(self, *args, **kwargs):
        super(MediaResourceForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('title'),
            Field('link'),
            Field('description'),
            Field('similar'),
            Field('partners'),
            Field('attachment'),
            Field('tags'),
            self.form_actions
        )


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField()
    confirm_email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean_confirm_email(self):
        new_email = self.cleaned_data.get('new_email')
        confirm_email = self.cleaned_data.get('confirm_email')
        if new_email and confirm_email:
            if new_email != confirm_email:
                raise forms.ValidationError("Emails don't match!")
        return confirm_email

    def save(self, user, commit=True):
        user.email = self.cleaned_data['new_email']
        if commit:
            user.save()
        return user


class YouthMapPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(YouthMapPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False