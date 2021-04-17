from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm,LeadModelForm
# Create your views here.

def landing_page(request):
    return render(request,'landing.html')

def lead_list(requests):
    # return HttpResponse("Hello World")
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(requests, 'leads/home_page.html', context)


def lead_detail(requests, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(requests, 'leads/lead_detail.html', context)


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

def lead_update(requests,pk):
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
        form = LeadModelForm(requests.POST,instance=lead)
        if form.is_valid:
            form.save()
            return redirect('/leads/')
    context = {
        'lead': lead,
        "form":form
    }
    return render(requests, "leads/lead_update.html", context)

def lead_delete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')