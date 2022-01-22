from django.contrib import admin

# Register your models here.
from .models import Participation, Voting, Option, PublicVote, AnonymousVote, Group
from django.contrib.auth.models import User

#admin.site.register(Voting)
#admin.site.register(Option)

class OptionInLine(admin.TabularInline):
    model = Option
    extra = 2

class VotingAdmin(admin.ModelAdmin):
    inlines = [OptionInLine]

admin.site.register(Voting, VotingAdmin)
admin.site.register(PublicVote)
admin.site.register(AnonymousVote)
admin.site.register(Participation)
admin.site.register(Group)