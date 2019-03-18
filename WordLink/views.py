from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from urllib.request import urlopen
from bs4 import BeautifulSoup
from .models import word_link
# Create your views here.
def Word_Link(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('Word_Link.html', context)
def Word_Link_Result(request):

    word_searched = request.POST['Keyword']
    url = "https://en.wikipedia.org/wiki/" + word_searched
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    type(soup)
    count = 0

    # get all para
    h1 = soup.find_all('p')

    # l is list of links
    l = []

    for all_p in h1:
        temp = all_p.find_all('a')
        # print(count,">>>")
        # print(temp)
        for ls in temp:
            t = ls.get('href')
            if t[0] == '/':
                l.append(t)

                count += 1
        if count >= 5:
            break

    strings = url.split('/')
    string = strings[0] + "//" + strings[2]
    result = ""
    for ls in l[:5]:
        result += string+ls+","

    result = result[:len(result)-1]


    wl=word_link()
    wl.result = result
    wl.word_searched=word_searched
    wl.user_id=11
    wl.save()
    res_arr=result.split(',')

    context={"results":res_arr}
    context.update(csrf(request))
    return render_to_response('Word_Link_Result.html', context)
