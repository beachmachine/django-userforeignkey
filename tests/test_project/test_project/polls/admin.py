from django.contrib import admin

from .models import Choice, Poll, ActualVote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently', 'created_by')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(ActualVote)
