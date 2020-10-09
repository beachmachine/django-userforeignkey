try:
    # Django 1.10 and above
    from django.urls import reverse
except:
    # Django 1.8 and 1.9
    from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login, logout

from .models import Choice, Poll, ActualVote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


@login_required
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)

    if 'choice' not in request.POST:
        return HttpResponseRedirect(reverse('polls:detail', args=(p.id,)))
    else:
        try:
            selected_choice = p.choices.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the poll voting form.
            return render(request, 'polls/detail.html', {
                'poll': p,
                'error_message': "Error: You didn't select a valid choice.",
            })
        else:
            if len(ActualVote.objects.filter(poll=p, user=request.user)) > 0:
                return render(request, 'polls/detail.html', {
                    'poll': p,
                    'error_message': "Error: You already voted!",
                })
            else:
                selected_choice.votes += 1
                selected_choice.save()

                vote = ActualVote()
                vote.choice = selected_choice
                vote.poll = p
                vote.save()

                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def login_view(request):
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('polls:index'))
            else:
                # Return a 'disabled account' error message
                return HttpResponse('Error: Account disabled', status=403)
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('Error: Invalid Login', status=403)
    else:
        return render(request, 'polls/templates/registration/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:index'))