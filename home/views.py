from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from .models import user


# Create your views here.
def index(request):
    if request.session.get('login') == "True":
        logged = True
        username = request.session['username']
    else:
        logged = False
        username = ""


    context = {"logged":logged,"username":username}
    context.update(csrf(request))
    return render_to_response('index.html', context)
def login(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('login.html', context)
def signup(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('signup.html', context)
def validate_login(request):
    if user.objects.filter(username=request.POST['name']).exists():
        already_exist=True
        user1=user.objects.get(username=request.POST['name'])
        if user1.password==request.POST['pass'] and user1.username==request.POST['name']:
            correct_credentials=True
        else:
            correct_credentials=False
    else:
        already_exist=False
        correct_credentials=False

    if correct_credentials==False:
        request.session['login']="False";
        request.session['username']=""
    else:
        request.session['login']='True';
        request.session['username']=request.POST['name']
    context = {"already_exist":already_exist,"correct_credentials":correct_credentials}
    context.update(csrf(request))
    return render_to_response('validate_login.html', context)
def validate_signup(request):

    if user.objects.filter(username=request.POST['name']).exists():
        already_exist=True
    else:
        user1 = user()
        user1.username = request.POST['name']
        user1.email = request.POST['email']
        user1.password = request.POST['pass']
        user1.save()
        already_exist=False

    context = {"already_exist":already_exist}
    context.update(csrf(request))
    return render_to_response('validate_signup.html', context)




