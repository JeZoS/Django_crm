from django.shortcuts import render,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginRequiredMixin

# Create your views here.
class AgentListView(OrganiserAndLoginRequiredMixin,generic.ListView):
    template_name = 'agents/agent_list.html'
    def get_queryset(self):
        organ = self.request.user.userprofile
        return Agent.objects.filter(organisation = organ)

class AgentCreateView(OrganiserAndLoginRequiredMixin,generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self,form):
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganiserAndLoginRequiredMixin,generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organ = self.request.user.userprofile
        return Agent.objects.filter(organisation = organ)


class AgentUpdateView(OrganiserAndLoginRequiredMixin,generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organ = self.request.user.userprofile
        return Agent.objects.filter(organisation = organ)

class AgentDeleteView(OrganiserAndLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = 'agent'
    
    def get_queryset(self):
        return Agent.objects.all()
    
    def get_success_url(self):
        organ = self.request.user.userprofile
        return Agent.objects.filter(organisation = organ)