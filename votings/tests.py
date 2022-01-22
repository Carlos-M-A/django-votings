from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.utils import timezone
# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Voting

def create_voting(question):
    now = timezone.now()
    tomorrow = now + datetime.timedelta(days=1)
    return Voting.objects.create(question_text=question, start_date=now, end_date=tomorrow)

class VotingModelTest(TestCase):
    def test_voting_is_finished(self):
        now = datetime.datetime.now()
        date_before_now = datetime.datetime(2022,1,8,12,12,0)
        voting = Voting(question_text='aaa', start_date=now, end_date=date_before_now)
        self.assertTrue(voting.is_finished)

class VotingViewTest(TestCase):
    def test_view_view(self):
        client = Client()
        voting = create_voting('nueva pregunta')
        response = client.get(reverse('voting:voting', args=(voting.id,)))
        self.assertEqual(voting, response.context['voting'])