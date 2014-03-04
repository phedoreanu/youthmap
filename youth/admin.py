from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from youth.models import Idea, Project, Activity, MetaResource, Tag, Organisation, Event, MediaResource, Experience, Profile, Education, Newsletter, Diploma, Speciality, Article, About


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1


class IdeaAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['title', 'activities', 'resources', 'tags']}),
    #     ('Date information', {'fields': ['start_date', 'end_date', 'pub_date']}),
    # ]
    # inlines = [ActivityInline]
    list_display = ('title', 'start_date', 'was_published_recently')
    list_filter = ['start_date']
    search_fields = ['title']
    date_hierarchy = 'start_date'


admin.site.register(Idea, IdeaAdmin)
admin.site.register(Project, ModelAdmin)
admin.site.register(MetaResource, ModelAdmin)
admin.site.register(Tag, ModelAdmin)
admin.site.register(Activity, ModelAdmin)
admin.site.register(Organisation, ModelAdmin)
admin.site.register(Experience, ModelAdmin)
admin.site.register(Education, ModelAdmin)
admin.site.register(Event, ModelAdmin)
admin.site.register(MediaResource, ModelAdmin)
admin.site.register(Profile, ModelAdmin)
admin.site.register(Newsletter, ModelAdmin)
admin.site.register(Diploma, ModelAdmin)
admin.site.register(Speciality, ModelAdmin)
admin.site.register(Article, ModelAdmin)
admin.site.register(About, ModelAdmin)