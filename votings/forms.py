from cProfile import label
from pyexpat import model
from attr import attr, attrs
from django import forms
from .models import Option, Organization, Voting, VotingStates
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput

CHOICES_VOTING_STATES = (
        (0, ''),
        (VotingStates.PLANNED, _('PLANNED')),
        (VotingStates.SCHEDULED, _('SCHEDULED')),
        (VotingStates.ACTIVE, _('ACTIVE')),
        (VotingStates.FINISHED, _('FINISHED')),
    )

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ( 'name_text',
                    'description_text')

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = (  'title_text', 
                    'question_text',
                    'explanation_text',
                    'are_votes_anonymous',
                    'assembly')
        labels = {
            'title_text': _('Title'),
        }
        help_texts = {
            'title_text': _('Some useful help text. Title text'),
        }
        error_messages = {
            'title_text': {
                'max_length': _("This title is too long."),
            },
        }
        widgets = {
            'assembly': forms.widgets.HiddenInput()
        }

class VotingDatesForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ('start_date', 'end_date')
        widgets = {
            'start_date': DateTimePickerInput(),
            'end_date': DateTimePickerInput(),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ( 'title_text',
                    'explanation_text')

class SearchVotingForm(forms.Form):
    text = forms.CharField(label="", max_length=100, required=False)
    state = forms.ChoiceField(label='state', choices=CHOICES_VOTING_STATES, required=False)
    date_since = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    date_until = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    id_assembly = forms.IntegerField(widget=forms.widgets.HiddenInput(), required=False)
    id_organization = forms.IntegerField(widget=forms.widgets.HiddenInput(), required=False)

class SearchMemberForm(forms.Form):
    text = forms.CharField(label="", max_length=100, required=False)
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    id_assembly = forms.IntegerField(widget=forms.widgets.HiddenInput(), required=False)