from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from .models import user
from Emails.models import emails
from WordLink.models import word_link


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

    context = {"already_exist":already_exist,"correct_credentials":correct_credentials,"username":request.POST['name']}
    context.update(csrf(request))
    return render_to_response('validate_login.html', context)
def validate_signup(request):

    if user.objects.filter(username=request.POST['name']).exists():
        already_exist=True
    else:
        user1 = user()
        user1.username = request.POST['name']
        user1.email = request.POST['email']
        print(request.POST['email'])
        user1.password = request.POST['pass']
        user1.save()
        already_exist=False

    context = {"already_exist":already_exist}
    context.update(csrf(request))
    return render_to_response('validate_signup.html', context)
def profile(request):
    username = request.COOKIES.get('username','')
    if username!='':
        if request.COOKIES['username']:
            logged=True
        else:
            logged=False
            #show error page and make him log first
        if user.objects.filter(username=username).exists():
            user1=user.objects.get(username=username)

        else:
            print("error occured")
            #lead them to error page
        email=user1.email



        result=[]
        url_searched=[]
        time_searched=[]
        ema=emails.objects.filter(username=username)
        print("users:")
        for u in ema:
            # print(u.username,u.url_searched,u.result,"hey you found me")
            result.append(u.result)
            url_searched.append(u.url_searched)
            time_searched.append(u.date_time)


        wolink=word_link.objects.filter(username=username)
        res=[]
        key=[]
        t_d=[]
        for u in wolink:
            # print(u.username,u.url_searched,u.result,"hey you found me")
            res.append(u.result)
            key.append(u.word_searched)
            t_d.append(u.date_time)

        #HERE WE WILL FETCH THE BASIC SCRAPPING DATA

        context={"email":email,"username":username,"logged":logged,"final_result1":zip(result,url_searched,time_searched),"final_result2":zip(res,key,t_d)}
        context.update(csrf(request))
        return render_to_response('profile.html', context)
    else:
        context = {"error":"Access Denied for this page"}
        context.update(csrf(request))
        return render_to_response('error.html', context)

def signout(request):
    response = HttpResponseRedirect('http://127.0.0.1:8000/home/index.html')
    request.session['login']="False"
    print("hell cookie")
    response.delete_cookie('csrftoken')
    response.delete_cookie('sessionid')
    print("hell cookie2 ")
    context={}
    context.update(csrf(request))
    return render_to_response('index.html', context)
def error(request):
    context = {"error":"Yeah this is error.html"}
    context.update(csrf(request))
    return render_to_response('error.html', context)

