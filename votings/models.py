from django.db import models
from django.contrib.auth.models import User
import datetime

class VotingStates():
    EDITABLE = 1
    READY = 2
    OPENED = 3
    CLOSED = 4


class Assembly(models.Model):
    name_text = models.CharField(max_length=128)
    description_text = models.TextField(max_length=256, blank=True)
    is_general = models.BooleanField(default=False)
    general_assembly = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_text


class Membership(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.start_date) + ' ----- ' + str(self.end_date)


class Voting(models.Model):
    title_text = models.CharField(max_length=128)
    question_text = models.CharField(max_length=256)
    explanation_text = models.TextField(max_length=512, blank=True)
    assembly = models.ForeignKey(Assembly, on_delete=models.RESTRICT)
    are_votes_anonymous = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    electorate_quantity = models.PositiveIntegerField(null=True, blank=True)
    votes_quantity = models.PositiveIntegerField(null=True, blank=True)
    state = models.PositiveSmallIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_text + ' (' + self.assembly.name_text + ')'

    def update_status(self):
        now = datetime.datetime.now()
        if self.end_date == None or self.start_date == None:
            self.state = VotingStates.EDITABLE
        elif now < self.start_date:
            self.state = VotingStates.READY
        elif now < self.end_date:
            self.state = VotingStates.OPENED
        elif now >= self.end_date:
            self.state = VotingStates.CLOSED


class Option(models.Model):
    index_number = models.IntegerField()
    title_text = models.CharField(max_length=128)
    explanation_text = models.TextField(max_length=512, blank=True)
    votes_quantity = models.PositiveIntegerField(null=True, blank=True)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)

    def __str__(self):
        return '(' + str(self.index_number) +  ') ' + self.title_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    option = models.ForeignKey(Option, on_delete=models.RESTRICT)

    def __str__(self):
        if self.user == None:
            return str(self.id) + ': ' + str(self.option.index_number)
        else:
            return str(self.user.id) + ': ' + str(self.option.index_number)


class Participation(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    participation_check = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.id) + ': ' + str(self.participation_check)


class Tag(models.Model):
    name_text = models.CharField(max_length=128)
    assembly = models.ForeignKey(Assembly, on_delete=models.RESTRICT)
    voting = models.ManyToManyField(Voting, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_text