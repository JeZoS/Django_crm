from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from leads.models import Agent


# Create your views here.
class AgentListView(LoginRequiredMixin,generic.ListView):
    template_name = 'agents/agent_list.html'
    def get_queryset(self):
        return Agent.objects.all()