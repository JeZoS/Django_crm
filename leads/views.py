from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead

# Create your views here.
def lead_list(requests):
    # return HttpResponse("Hello World")
    leads = Lead.objects.all();
    context = {
        "leads":leads
    }
    return render(requests,'leads/home_page.html',context)

def lead_detail(requests,pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }
    return render(requests,'leads/lead_detail.html',context)