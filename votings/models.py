from django.db import models
from django.contrib.auth.models import User
import datetime

class VotingStates():
    EDITABLE = 1
    NOT_EDITABLE_AND_READY = 2
    STARTED_AND_IN_PROGRESS = 3
    FINISHED_AND_CLOSED = 4


class Group(models.Model):
    name_text = models.CharField(max_length=128)
    scope_description = models.CharField(max_length=128, blank=True)
    is_principal = models.BooleanField(default=False)
    parent_group = models.ForeignKey('self', on_delete=models.RESTRICT, null=True)
    manager = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_text


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.start_date) + ' - ' + str(self.end_date)


class Voting(models.Model):
    title_text = models.CharField(max_length=128)
    question_text = models.CharField(max_length=256)
    explanation_text = models.CharField(max_length=512, blank=True)
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    is_anonymous = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    deadline_to_edit = models.DateTimeField(null=True)
    electorate_quantity = models.PositiveIntegerField(null=True)
    votes_quantity = models.PositiveIntegerField(null=True)
    none_of_the_options_quantity = models.PositiveIntegerField(null=True)
    state = models.PositiveSmallIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_text + ' (' + self.group.name_text + ')'

    def is_started(self):
        if self.start_date == None:
            return False
        else: 
            now = datetime.datetime.now()
            return now >= self.start_date and now < self.end_date

    def is_finished(self):
        if self.end_date == None:
            return False
        else: 
            now = datetime.datetime.now()
            return now >= self.end_date

    def is_editable(self):
        if self.deadline_to_edit == None:
            return True
        else:
            now = datetime.datetime.now()
            return now < self.deadline_to_edit


class Option(models.Model):
    index_number = models.IntegerField()
    title_text = models.CharField(max_length=128)
    explanation_text = models.CharField(max_length=512, blank=True)
    votes_quantity = models.PositiveIntegerField(null=True)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)

    def __str__(self):
        return '(' + str(self.index_number) +  ') ' + self.title_text


class PublicVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    option = models.ForeignKey(Option, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.user.id) +': ' + str(self.option.index_number)


class AnonymousVote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id) +': ' + str(self.option.index_number)


class Participation(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    participation_check = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.id + ': ' + str(self.participation_check))


class Tag(models.Model):
    name_text = models.CharField(max_length=128)
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    voting = models.ManyToManyField(Voting)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_text