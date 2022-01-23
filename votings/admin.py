from django.contrib import admin

# Register your models here.
from .models import Assembly, Membership, Participation, Tag, Voting, Option, Vote
from django.contrib.auth.models import User

#admin.site.register(Voting)
#admin.site.register(Option)

class OptionInLine(admin.TabularInline):
    model = Option
    extra = 2

class VotingAdmin(admin.ModelAdmin):
    inlines = [OptionInLine]

admin.site.register(Voting, VotingAdmin)
admin.site.register(Vote)
admin.site.register(Participation)
admin.site.register(Tag)
admin.site.register(Assembly)
admin.site.register(Membership)