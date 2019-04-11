from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from urllib.request import urlopen
from bs4 import BeautifulSoup
from .models import word_link
# Create your views here.
def Word_Link(request):
    try:
        if request.GET['q']=='':
            print("OK this is the error")
            request.COOKIES['username'] = request.GET['q']
            if request.COOKIES['username']:
                logged=True
            else:
                logged=False
            context = {'username':request.GET['q'],"logged":logged}

            context.update(csrf(request))

            return render_to_response('Word_Link.html', context)
    except:
        context = {"error":"Direct Access Denied"}
        context.update(csrf(request))
        return render_to_response('error.html', context)
    # else:
    #     context = {}
    #
    #     context.update(csrf(request))
    #     return render_to_response('error.html', context)
def Word_Link_Result(request):
    # get the request parameter i.e. keyword entered
    try:
        word_searched = request.POST['Keyword']
    except:
            context = {"error": "Direct Access Denied"}
            context.update(csrf(request))
            return render_to_response('error.html', context)
    # word_searched = "Binary_number"
    # initial wikipedia url
    wiki_url = "https://en.wikipedia.org/wiki/"

    # initialize url queue
    url_queue = []
    # initialize the queue with the user entered wiki_url+keyword
    url_queue.append(wiki_url + word_searched)
    # so it will become https://en.wikipedia.org/wiki/<keyword>
    # for example https://en.wikipedia.org/wiki/binary

    urls_searched = []
    urls_heading = []

    # run the following loop for 5 times
    # runiing loop 5 times means poping the elements 5 times

    # url to its linked url map
    # url in string and linked url in list of string
    dict_url_linkurl = {}
    links_count = 0
    while links_count <= 5:
        # pop the element
        url = url_queue.pop(0)

        # links contain the links in current url
        links = []

        print(url)
        # open the url
        try:
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
        except:
            continue

        # get the h1 heading of the page
        h1 = soup.h1.contents[0]

        # get all paragraph in a list
        paragraph_list = soup.find_all('p')

        for paragraph in paragraph_list:
            # from paragraph find all <a> tags that contain link
            # a_tag_list
            a_tag_list = paragraph.find_all('a')

            # count for finding only 5 links from this page
            count = 0

            for a in a_tag_list:
                # get href of one link
                linked_url = a.get('href')

                try:
                    # this if condition ignores the links on the same page and only get link to another page
                    if linked_url[0] == '/' and linked_url[1]!='/':
                        links.append(linked_url)
                        url_queue.append(wiki_url + linked_url[6:])
                        count += 1
                    if count >= 5:
                        break
                except:
                    continue
            if count >= 5:
                break

        # append the poped element in keywords_searched
        urls_searched.append(url)
        urls_heading.append(h1)

        # if count is less than 5 Show appropriate message
        # show message here

        print(links)
        print(url_queue)
        # link are of format "/<keyword>"
        # links have list of links for current url so map it
        n_links = []
        for e_link in links:
            s = e_link.split('/')
            n_links.append(s[-1])
        if str(url) not in dict_url_linkurl:
            dict_url_linkurl[str(url)] = n_links
            links_count += 1
    #for testing purpose
    #print(dict_url_linkurl)


    if request.COOKIES['username']:
        logged=True
    else:
        logged=False
    #now we can store the dictionary to the database
    wl=word_link()
    if logged:
        wl.username=request.COOKIES['username']

    wl.result = str(dict_url_linkurl)
    wl.word_searched=word_searched

    wl.save()

    zeroth=urls_searched[0]
    first=urls_searched[1]
    second=urls_searched[2]
    third=urls_searched[3]
    fourth=urls_searched[4]
    fifth=urls_searched[5]


    context={"zeroth":zeroth,"first":first,"second":second,"third":third,"fourth":fourth,"fifth":fifth,
             "zeroth_heading":urls_heading[0],"first_heading":urls_heading[1],"second_heading":urls_heading[2],"third_heading":urls_heading[3],
             "fourth_heading":urls_heading[4],"fifth_heading":urls_heading[5],"list_link_1":dict_url_linkurl[urls_searched[1]][:5],"list_link_2":dict_url_linkurl[urls_searched[2]][:5],
             "list_link_3":dict_url_linkurl[urls_searched[3]][:5],"list_link_4":dict_url_linkurl[urls_searched[4]][:5],"list_link_5":dict_url_linkurl[urls_searched[5]][:5],"username":request.COOKIES['username'],"logged":logged}
    context.update(csrf(request))
    return render_to_response('Word_Link_Result.html', context)
