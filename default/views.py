from django.shortcuts import render
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView, DeleteView
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

class PollVote(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        op = Option.objects.get(id=self.kwargs['oid'])
        op.count += 1
        op.save()
        return "/poll/{}/".format(op.poll_id)

class PollCreate(CreateView):
    model = Poll
    fields = ['subject' , 'desc']
    success_url = '/poll/'
    
    def get_success_url(self):
        return "/poll/{}/".format(self.object.id)

class PollEdit(UpdateView):
    model = Poll
    fields = ['subject','desc']

    def get_success_url(self):
        return "/poll/{}/".format(self.object.id)
class PollDelete(DeleteView):
    model = Poll
    success_url = '/poll/'

class OptionCreate(CreateView):
    model = Option
    fields = ['title']
    templete_name = 'default/poll_form.html'

    def form_valid(self, form):
        form.instance.poll_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return "/poll/{}/".format(self.object.poll_id)

class OptionEdit(UpdateView):
    model = Option
    fields = ['title']
    pk_url_kwarg='oid'
    template_name='default/poll_form.html'

    def get_success_url(self):
        return "/poll/{}/".format(self.object.poll_id)

class OptionDelete(DeleteView):
    model = Option
    pk_url_kwarg='oid'
    def get_success_url(self):
        return "/poll/{}/".format(self.object.poll_id)