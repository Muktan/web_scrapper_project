from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uopen


# Create your views here.

def news_result(request):
	try:
		if request.GET['q']!='':
			request.COOKIES['username'] =request.GET['q']
			username=request.GET['q']
			logged=True
			news_url = "https://news.google.com/news/rss"
			Client = uopen(news_url)
			xml_page = Client.read()
			Client.close()

			page_soup = soup(xml_page, "xml")
			news_list = page_soup.findAll("item")

			res_arr = []
			res_arr1 = []
			for i in news_list:
				res_arr.append([i.title.text, i.pubDate.text])
				res_arr1.append(i.link.text)

			context = {"results": zip(res_arr, res_arr1), "username": username, "logged": logged}
			context.update(csrf(request))
			return render_to_response('news_result.html', context)
		else:
			logged=False
			news_url = "https://news.google.com/news/rss"
			Client = uopen(news_url)
			xml_page = Client.read()
			Client.close()

			page_soup = soup(xml_page, "xml")
			news_list = page_soup.findAll("item")

			res_arr = []
			res_arr1 = []
			for i in news_list:
				res_arr.append([i.title.text, i.pubDate.text])
				res_arr1.append(i.link.text)

			context = {"results": zip(res_arr, res_arr1),"logged": logged}
			context.update(csrf(request))
			return render_to_response('news_result.html', context)
	except:
		logged=False
		news_url = "https://news.google.com/news/rss"
		Client = uopen(news_url)
		xml_page = Client.read()
		Client.close()

		page_soup = soup(xml_page, "xml")
		news_list = page_soup.findAll("item")

		res_arr = []
		res_arr1 = []
		for i in news_list:
			res_arr.append([i.title.text, i.pubDate.text])
			res_arr1.append(i.link.text)

		context = {"results": zip(res_arr, res_arr1),"logged":logged}
		context.update(csrf(request))
		return render_to_response('news_result.html', context)
