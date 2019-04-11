from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from urllib.request import urlopen
from bs4 import BeautifulSoup
from .models import emails
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
# Create your views here.
def Emails(request):
    try:
        request.COOKIES['username']=request.GET['q']
    except:
        context = {"error": "Direct Access Denied"}
        context.update(csrf(request))
        return render_to_response('error.html', context)
    if request.COOKIES['username']:
        logged=True
    else:
        logged=False
    context = {'username':request.GET['q'],"logged":logged}
    context.update(csrf(request))

    return render_to_response('Emails.html', context)

def Emails_Result(request):
    try:
        url_searched = request.POST['url']
    except:
        context = {"error": "Direct Access Denied"}
        context.update(csrf(request))
        return render_to_response('error.html', context)


    # a queue of urls to be crawled
    new_urls = deque([url_searched])

    # a set of urls that we have already crawled
    processed_urls = set()

    # a set of crawled emails
    email = set()

    # process urls one by one until we exhaust the queue
    while len(new_urls):

        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        processed_urls.add(url)

        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        # get url's content
       # print("Processing %s" % url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors
            continue

        # extract all email addresses and add them into the resulting set
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        email.update(new_emails)

        # create a beutiful soup for the html document
    # soup = BeautifulSoup(response.text)

    # find and process all the anchors in the document
    # for anchor in soup.find_all("a"):
    # extract link url from the anchor
    #    link = anchor.attrs["href"] if "href" in anchor.attrs else ''
    # resolve relative links
    #   if link.startswith('/'):
    #      link = base_url + link
    # elif not link.startswith('http'):
    #    link = path + link
    # add the new url to the queue if it was not enqueued nor processed yet
    # if not link in new_urls and not link in processed_urls:
    #    new_urls.append(link)

    res_arr=[]
    for i in email :
        res_arr.append(i)
    if request.COOKIES['username']:
        logged=True
    else:
        logged=False
    wl=emails()
    wl.result = email
    wl.url_searched=url_searched
    if logged:
        wl.username=request.COOKIES['username']
    wl.save()

    context={"results": res_arr,"url_searched":url_searched,"username":request.COOKIES['username'],"logged":logged}
    context.update(csrf(request))
    return render_to_response('Emails_Result.html', context)

def Emails_Downloads(request):
    import reportlab
    import io
    from django.http import FileResponse
    from reportlab.pdfgen import canvas

    url_searched = request.POST['url']
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = " + url_searched +".pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    for i in results:
        p.drawString(0, 0, i)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response