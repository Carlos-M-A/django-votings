from django import forms
from .models import Option, Voting

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = (  'title_text', 
                    'question_text',
                    'explanation_text',
                    'are_votes_anonymous')

class VotingDatesForm(forms.ModelForm):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ( 'title_text',
                    'explanation_text')