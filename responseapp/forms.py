from django import forms
from responseapp.udchoices import *

class MyForm(forms.Form):
	#c = [('1', 'Ch1'), ('2', 'Ch2'), ('3', 'Ch3'),]

    name = forms.CharField(label='Enter your name', max_length=100, widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))
    email = forms.EmailField(label='Enter your email', max_length=100)
    url = forms.URLField(label='Submit a link you want us scrapped ', max_length=100)
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='', widget=forms.Select(), label='How do you feel after using our site?')
    feedback = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "50", 'rows': "10", }))
    #happy = forms.ChoiceField(label='Choices', choices=[('1', 'Ch1'), ('2', 'Ch2'), ('3', 'Ch3')], widget=forms.Select())
    #authors = forms.ModelMultipleChoiceField()

    name.widget.attrs.update({'class': 'special'})
	#email.widget.attrs.update(size='40')