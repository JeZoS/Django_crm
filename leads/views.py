from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserAndLoginRequiredMixin


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = 'landing.html'


def landing_page(request):
    return render(request, 'landing.html')


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/home_page.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()
        if user.is_organiser:
            queryset = queryset.filter(
                organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = queryset.filter(
                organisation=user.agent.organisation, agent__isnull=False)
            print(queryset)
            queryset = queryset.filter(agent__user=user)
            print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


def lead_list(requests):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(requests, 'leads/home_page.html', context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


def lead_detail(requests, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(requests, 'leads/lead_detail.html', context)


class LeadCreateView(OrganiserAndLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        send_mail(
            subject="A Lead has been created",
            message="Go to the site to see the lead",
            from_email='test@test.com',
            recipient_list=["test2@test.com"]
        )
        data = form.cleaned_data
        Lead.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            agent=data['agent'],
            organisation=self.request.user.userprofile
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(requests):
    form = LeadModelForm
    if requests.method == "POST":
        form = LeadModelForm(requests.POST)
        if form.is_valid():
            form.save()
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # age = form.cleaned_data['age']
            # agent = form.cleaned_data['agent']
            # Lead.objects.create(first_name=first_name,
            #                     last_name=last_name, age=age, agent=agent)
            print("created")
            return redirect('/leads/')
    context = {
        'form': form
    }
    return render(requests, "leads/lead_create.html", context)


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')


def lead_update(requests, pk):
    lead = Lead.objects.get(id=pk)
    # form = LeadForm()
    # if requests.method == "POST":
    #     form = LeadForm(requests.POST)
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         # agent = form.cleaned_data['agent']
    #         agent = Agent.objects.first()
    #         lead.first_name = first_name
    #         lead.last_name = last_name
    #         lead.age = age
    #         lead.save()
    form = LeadModelForm(instance=lead)
    if requests.method == "POST":
        form = LeadModelForm(requests.POST, instance=lead)
        if form.is_valid:
            form.save()
            return redirect('/leads/')
    context = {
        'lead': lead,
        "form": form
    }
    return render(requests, "leads/lead_update.html", context)


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()
    # form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


# class AssignAgentView(OrganiserAndLoginRequiredMixin):