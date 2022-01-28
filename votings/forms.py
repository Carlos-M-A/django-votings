from django import forms
from .models import Option, Voting
from django.utils.translation import ugettext_lazy as _

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = (  'title_text', 
                    'question_text',
                    'explanation_text',
                    'are_votes_anonymous')
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

class VotingDatesForm(forms.ModelForm):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ( 'title_text',
                    'explanation_text')