from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Poll, Option

# Create your views here.
def poll_list(req):
    data = Poll.objects.all()
    return render(req, 'poll_list.html', {'polls':data})

class PollList(ListView):
    model = Poll

class PollDetail(DetailView):
    model = Poll

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['option_list'] = Option.objects.filter(poll_id=self.kwargs['pk'])
        return ctx
