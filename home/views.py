from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf


# Create your views here.
def index(request):
    context = {'abc': "heyyy"}
    context.update(csrf(request))
    return render_to_response('index.html', context)
