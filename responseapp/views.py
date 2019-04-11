from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf

from responseapp.forms import MyForm
from django.template import loader
from django.http import HttpResponse
from .models import feedback as fb

def responseform(request):
    if request.method == 'POST':
        myForm = MyForm(request.POST)

        if myForm.is_valid():
            name = myForm.cleaned_data['name']
            email = myForm.cleaned_data['email']
            url = myForm.cleaned_data['url']
            feedback = myForm.cleaned_data['feedback']
            # happy = myForm.cleaned_data['happy']

            context = {
                'name': name,
                'email': email,
                'url': url,
                'feedback': feedback

            }
            user_feedback=fb()
            user_feedback.name=name
            user_feedback.feedback=feedback
            user_feedback.email=email
            user_feedback.link=url
            user_feedback.save()
            #
            context.update(csrf(request))
            return render_to_response('index.html', context)
        else:
            context={"fill":"True"}
            context.update(csrf(request))
            return render_to_response('responseform.html', context)


    else:
        form = MyForm()

    return render(request, 'responseform.html', {'form': form});
