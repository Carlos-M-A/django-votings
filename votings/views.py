from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Option, Voting

def index(request):
    voting_list = Voting.objects.all()
    context = {
        'voting_list':voting_list,
    }
    return render(request, 'votings/index.html', context)

def voting(request, voting_id):
    try:
        voting = Voting.objects.get(pk=voting_id)
        context = {
            'voting':voting
        }
    except Voting.DoesNotExist:
        raise Http404('Voting does not exist')
    return render(request, 'votings/voting.html', context)

def options(request, voting_id):
    if request.method == 'POST':
        voting = Voting.objects.get(pk=voting_id)
        new_option = Option(index_number=1, title_text=request.POST['answer'], voting=voting)
        new_option.save()
        #options_list = Option.objects.filter(voting_id=voting_id)
        #return render(request, 'votings/option.html', {'options_list':options_list, 'voting_id':voting_id})
        return HttpResponseRedirect(reverse('votings:options', args=(voting.id,)))
    else:
        options_list = Option.objects.filter(voting_id=voting_id)
        return render(request, 'votings/options.html', {'options_list':options_list, 'voting_id':voting_id})

def option(request, option_id):
    option = get_object_or_404(Option, pk=option_id)
    return render(request, 'votings/option.html', {'option':option})

class OptionView(generic.DeleteView):
    model = Option
    template_name = 'votings/option.html'