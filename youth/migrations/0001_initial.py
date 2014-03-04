# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table(u'youth_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('icon', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('svg_icon', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tooltip', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
        ))
        db.send_create_signal(u'youth', ['Activity'])

        # Adding model 'Tag'
        db.create_table(u'youth_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal(u'youth', ['Tag'])

        # Adding model 'Language'
        db.create_table(u'youth_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('proficiency', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
        ))
        db.send_create_signal(u'youth', ['Language'])

        # Adding model 'Article'
        db.create_table(u'youth_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 11, 0, 0), auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'youth', ['Article'])

        # Adding M2M table for field tags on 'Article'
        m2m_table_name = db.shorten_name(u'youth_article_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'youth.article'], null=False)),
            ('tag', models.ForeignKey(orm[u'youth.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'tag_id'])

        # Adding model 'Newsletter'
        db.create_table(u'youth_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_sent_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'youth', ['Newsletter'])

        # Adding model 'Relationship'
        db.create_table(u'youth_relationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='following_set', to=orm['auth.User'])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='followers_set', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'youth', ['Relationship'])

        # Adding model 'Profile'
        db.create_table(u'youth_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('interests', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('future_plans', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Country'])),
            ('availability', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('privacy', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('views', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 11, 0, 0), auto_now_add=True, blank=True)),
            ('other_field_of_activity', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'youth', ['Profile'])

        # Adding M2M table for field field_of_activity on 'Profile'
        m2m_table_name = db.shorten_name(u'youth_profile_field_of_activity')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'youth.profile'], null=False)),
            ('activity', models.ForeignKey(orm[u'youth.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'activity_id'])

        # Adding M2M table for field tags on 'Profile'
        m2m_table_name = db.shorten_name(u'youth_profile_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'youth.profile'], null=False)),
            ('tag', models.ForeignKey(orm[u'youth.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'tag_id'])

        # Adding model 'Organisation'
        db.create_table(u'youth_organisation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Country'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'])),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('values', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mission', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('objectives', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target_group', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('activities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('achievements', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('partners', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('level_of_activity', self.gf('django.db.models.fields.CharField')(default='LOC', max_length=3, blank=True)),
            ('number_of_members', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('contact_person_name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('official_position', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owner_set', to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 11, 0, 0), auto_now_add=True, blank=True)),
            ('views', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('other_field_of_activity', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'youth', ['Organisation'])

        # Adding M2M table for field field_of_activity on 'Organisation'
        m2m_table_name = db.shorten_name(u'youth_organisation_field_of_activity')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organisation', models.ForeignKey(orm[u'youth.organisation'], null=False)),
            ('activity', models.ForeignKey(orm[u'youth.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organisation_id', 'activity_id'])

        # Adding M2M table for field tags on 'Organisation'
        m2m_table_name = db.shorten_name(u'youth_organisation_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organisation', models.ForeignKey(orm[u'youth.organisation'], null=False)),
            ('tag', models.ForeignKey(orm[u'youth.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organisation_id', 'tag_id'])

        # Adding model 'Experience'
        db.create_table(u'youth_experience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_of_institution', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('field_of_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['youth.Activity'], null=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Country'], null=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'], null=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['youth.Profile'], null=True)),
        ))
        db.send_create_signal(u'youth', ['Experience'])

        # Adding model 'Diploma'
        db.create_table(u'youth_diploma', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'youth', ['Diploma'])

        # Adding model 'Speciality'
        db.create_table(u'youth_speciality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'youth', ['Speciality'])

        # Adding model 'Education'
        db.create_table(u'youth_education', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('institution_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('diploma', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['youth.Diploma'], unique=True)),
            ('speciality', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['youth.Speciality'], unique=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Country'], null=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'], null=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('qualifications', self.gf('django.db.models.fields.TextField')()),
            ('skills', self.gf('django.db.models.fields.TextField')()),
            ('courses', self.gf('django.db.models.fields.TextField')()),
            ('official_website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['youth.Profile'], null=True)),
        ))
        db.send_create_signal(u'youth', ['Education'])

        # Adding model 'Idea'
        db.create_table(u'youth_idea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Country'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('problem_addressed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slogan', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('objectives', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('milestones', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('other_needs', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('budget', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('visibility', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('background', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'youth', ['Idea'])

        # Adding M2M table for field field_of_activity on 'Idea'
        m2m_table_name = db.shorten_name(u'youth_idea_field_of_activity')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'youth.idea'], null=False)),
            ('activity', models.ForeignKey(orm[u'youth.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'activity_id'])

        # Adding M2M table for field resources on 'Idea'
        m2m_table_name = db.shorten_name(u'youth_idea_resources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'youth.idea'], null=False)),
            ('metaresource', models.ForeignKey(orm[u'youth.metaresource'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'metaresource_id'])

        # Adding M2M table for field resources_needed on 'Idea'
        m2m_table_name = db.shorten_name(u'youth_idea_resources_needed')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'youth.idea'], null=False)),
            ('metaresource', models.ForeignKey(orm[u'youth.metaresource'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'metaresource_id'])

        # Adding M2M table for field tags on 'Idea'
        m2m_table_name = db.shorten_name(u'youth_idea_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'youth.idea'], null=False)),
            ('tag', models.ForeignKey(orm[u'youth.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'tag_id'])

        # Adding model 'Project'
        db.create_table(u'youth_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Country'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('problem_addressed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slogan', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('objectives', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('milestones', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('other_needs', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('budget', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('visibility', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'youth', ['Project'])

        # Adding M2M table for field field_of_activity on 'Project'
        m2m_table_name = db.shorten_name(u'youth_project_field_of_activity')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'youth.project'], null=False)),
            ('activity', models.ForeignKey(orm[u'youth.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'activity_id'])

        # Adding M2M table for field resources on 'Project'
        m2m_table_name = db.shorten_name(u'youth_project_resources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'youth.project'], null=False)),
            ('metaresource', models.ForeignKey(orm[u'youth.metaresource'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'metaresource_id'])

        # Adding M2M table for field resources_needed on 'Project'
        m2m_table_name = db.shorten_name(u'youth_project_resources_needed')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'youth.project'], null=False)),
            ('metaresource', models.ForeignKey(orm[u'youth.metaresource'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'metaresource_id'])

        # Adding M2M table for field tags on 'Project'
        m2m_table_name = db.shorten_name(u'youth_project_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'youth.project'], null=False)),
            ('tag', models.ForeignKey(orm[u'youth.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'tag_id'])

        # Adding model 'MetaResource'
        db.create_table(u'youth_metaresource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'youth', ['MetaResource'])

        # Adding M2M table for field tags on 'MetaResource'
        m2m_table_name = db.shorten_name(u'youth_metaresource_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metaresource', models.ForeignKey(orm[u'youth.metaresource'], null=False)),
            ('tag', models.ForeignKey(orm[u'youth.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['metaresource_id', 'tag_id'])

        # Adding model 'Event'
        db.create_table(u'youth_event', (
            (u'metaresource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['youth.MetaResource'], unique=True, primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.Country'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities_light.City'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('guests', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('participants', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('partners', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('program', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('result', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 11, 0, 0), auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'youth', ['Event'])

        # Adding M2M table for field field_of_activity on 'Event'
        m2m_table_name = db.shorten_name(u'youth_event_field_of_activity')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'youth.event'], null=False)),
            ('activity', models.ForeignKey(orm[u'youth.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'activity_id'])

        # Adding model 'MediaResource'
        db.create_table(u'youth_mediaresource', (
            (u'metaresource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['youth.MetaResource'], unique=True, primary_key=True)),
            ('similar', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('partners', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 11, 0, 0), auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'youth', ['MediaResource'])


    def backwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table(u'youth_activity')

        # Deleting model 'Tag'
        db.delete_table(u'youth_tag')

        # Deleting model 'Language'
        db.delete_table(u'youth_language')

        # Deleting model 'Article'
        db.delete_table(u'youth_article')

        # Removing M2M table for field tags on 'Article'
        db.delete_table(db.shorten_name(u'youth_article_tags'))

        # Deleting model 'Newsletter'
        db.delete_table(u'youth_newsletter')

        # Deleting model 'Relationship'
        db.delete_table(u'youth_relationship')

        # Deleting model 'Profile'
        db.delete_table(u'youth_profile')

        # Removing M2M table for field field_of_activity on 'Profile'
        db.delete_table(db.shorten_name(u'youth_profile_field_of_activity'))

        # Removing M2M table for field tags on 'Profile'
        db.delete_table(db.shorten_name(u'youth_profile_tags'))

        # Deleting model 'Organisation'
        db.delete_table(u'youth_organisation')

        # Removing M2M table for field field_of_activity on 'Organisation'
        db.delete_table(db.shorten_name(u'youth_organisation_field_of_activity'))

        # Removing M2M table for field tags on 'Organisation'
        db.delete_table(db.shorten_name(u'youth_organisation_tags'))

        # Deleting model 'Experience'
        db.delete_table(u'youth_experience')

        # Deleting model 'Diploma'
        db.delete_table(u'youth_diploma')

        # Deleting model 'Speciality'
        db.delete_table(u'youth_speciality')

        # Deleting model 'Education'
        db.delete_table(u'youth_education')

        # Deleting model 'Idea'
        db.delete_table(u'youth_idea')

        # Removing M2M table for field field_of_activity on 'Idea'
        db.delete_table(db.shorten_name(u'youth_idea_field_of_activity'))

        # Removing M2M table for field resources on 'Idea'
        db.delete_table(db.shorten_name(u'youth_idea_resources'))

        # Removing M2M table for field resources_needed on 'Idea'
        db.delete_table(db.shorten_name(u'youth_idea_resources_needed'))

        # Removing M2M table for field tags on 'Idea'
        db.delete_table(db.shorten_name(u'youth_idea_tags'))

        # Deleting model 'Project'
        db.delete_table(u'youth_project')

        # Removing M2M table for field field_of_activity on 'Project'
        db.delete_table(db.shorten_name(u'youth_project_field_of_activity'))

        # Removing M2M table for field resources on 'Project'
        db.delete_table(db.shorten_name(u'youth_project_resources'))

        # Removing M2M table for field resources_needed on 'Project'
        db.delete_table(db.shorten_name(u'youth_project_resources_needed'))

        # Removing M2M table for field tags on 'Project'
        db.delete_table(db.shorten_name(u'youth_project_tags'))

        # Deleting model 'MetaResource'
        db.delete_table(u'youth_metaresource')

        # Removing M2M table for field tags on 'MetaResource'
        db.delete_table(db.shorten_name(u'youth_metaresource_tags'))

        # Deleting model 'Event'
        db.delete_table(u'youth_event')

        # Removing M2M table for field field_of_activity on 'Event'
        db.delete_table(db.shorten_name(u'youth_event_field_of_activity'))

        # Deleting model 'MediaResource'
        db.delete_table(u'youth_mediaresource')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cities_light.city': {
            'Meta': {'unique_together': "(('region', 'name'),)", 'object_name': 'City'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'feature_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'population': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Region']", 'null': 'True', 'blank': 'True'}),
            'search_names': ('cities_light.models.ToSearchTextField', [], {'default': "''", 'max_length': '4000', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"})
        },
        u'cities_light.country': {
            'Meta': {'object_name': 'Country'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'code2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"}),
            'tld': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'blank': 'True'})
        },
        u'cities_light.region': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'Region'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geoname_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'youth.activity': {
            'Meta': {'ordering': "['order']", 'object_name': 'Activity'},
            'icon': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'svg_icon': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'tooltip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        },
        u'youth.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 11, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'youth.diploma': {
            'Meta': {'object_name': 'Diploma'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'youth.education': {
            'Meta': {'object_name': 'Education'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']", 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']", 'null': 'True'}),
            'courses': ('django.db.models.fields.TextField', [], {}),
            'diploma': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['youth.Diploma']", 'unique': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'official_website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['youth.Profile']", 'null': 'True'}),
            'qualifications': ('django.db.models.fields.TextField', [], {}),
            'skills': ('django.db.models.fields.TextField', [], {}),
            'speciality': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['youth.Speciality']", 'unique': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'youth.event': {
            'Meta': {'object_name': 'Event', '_ormbases': [u'youth.MetaResource']},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'field_of_activity': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Activity']", 'symmetrical': 'False'}),
            'guests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'metaresource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['youth.MetaResource']", 'unique': 'True', 'primary_key': 'True'}),
            'participants': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'partners': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'program': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 11, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'youth.experience': {
            'Meta': {'object_name': 'Experience'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']", 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'field_of_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['youth.Activity']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_of_institution': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['youth.Profile']", 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'youth.idea': {
            'Meta': {'object_name': 'Idea'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'background': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'field_of_activity': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Activity']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'objectives': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_needs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'problem_addressed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.MetaResource']", 'symmetrical': 'False'}),
            'resources_needed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'youth_idea_needed'", 'symmetrical': 'False', 'to': u"orm['youth.MetaResource']"}),
            'slogan': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visibility': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'})
        },
        u'youth.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'proficiency': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'})
        },
        u'youth.mediaresource': {
            'Meta': {'object_name': 'MediaResource', '_ormbases': [u'youth.MetaResource']},
            u'metaresource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['youth.MetaResource']", 'unique': 'True', 'primary_key': 'True'}),
            'partners': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 11, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'similar': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'youth.metaresource': {
            'Meta': {'object_name': 'MetaResource'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['auth.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'youth.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        u'youth.organisation': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Organisation'},
            'achievements': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'activities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']"}),
            'contact_person_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'field_of_activity': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Activity']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_of_activity': ('django.db.models.fields.CharField', [], {'default': "'LOC'", 'max_length': '3', 'blank': 'True'}),
            'mission': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_members': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'objectives': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'official_position': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'other_field_of_activity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_set'", 'to': u"orm['auth.User']"}),
            'partners': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 11, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Tag']", 'symmetrical': 'False'}),
            'target_group': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'values': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'youth.profile': {
            'Meta': {'object_name': 'Profile'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'availability': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'field_of_activity': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['youth.Activity']", 'null': 'True', 'blank': 'True'}),
            'future_plans': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'other_field_of_activity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 11, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'views': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'youth.project': {
            'Meta': {'object_name': 'Project'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'field_of_activity': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Activity']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'objectives': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_needs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'problem_addressed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.MetaResource']", 'symmetrical': 'False'}),
            'resources_needed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'youth_project_needed'", 'symmetrical': 'False', 'to': u"orm['youth.MetaResource']"}),
            'slogan': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['youth.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visibility': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'})
        },
        u'youth.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'following_set'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'followers_set'", 'to': u"orm['auth.User']"})
        },
        u'youth.speciality': {
            'Meta': {'ordering': "['name']", 'object_name': 'Speciality'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'youth.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['youth']