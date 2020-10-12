from django.shortcuts import render, redirect, get_object_or_404
from bs4 import BeautifulSoup
from eldar import build_query
import requests
import re
from main.models import Search, Document


def parse_docements():
    Document.objects.all().delete()
    tut_by_page = requests.get('https://www.tut.by')
    assert tut_by_page.status_code == 200
    soup = BeautifulSoup(tut_by_page.text, 'html.parser')
    for href_tag in soup.find_all(class_=re.compile('io-block-link')):
        href = href_tag.get('href')
        page = requests.get(href)
        if page.status_code == 200:
            doc_soup = BeautifulSoup(page.text, 'html.parser')
            try:
                title = doc_soup.find(itemprop='headline').text
                article_body = doc_soup.find(itemprop='articleBody')
                text = ''
                for p in article_body.find_all('p'):
                    text += p.text
                snippet = ''
                for sent in text.split('.'):
                    if len(snippet + sent + '.') <= 300:
                        snippet += sent + '.'
                if Document.objects.count() < 100:
                    Document.objects.update_or_create(title=title, defaults={'text': text, 'snippet': snippet, 'url': href})
                else:
                    return
            except AttributeError:
                continue


def index(request):
    return render(request, 'main/index.html')


def rebuild(request):
    if request.method == 'GET':
        return render(request, 'main/rebuild_base.html')
    if request.method == 'POST':
        parse_docements()
        return redirect('search')


def search_page(request):
    if request.method == 'GET':
        return render(request, 'main/search.html')
    if request.method == 'POST':
        query = request.POST['query']
        search, _ = Search.objects.get_or_create(query=query)
        return redirect('result', search_id=search.id)

def help(request):
    return render(request, 'main/help.html')


def results(request, search_id):
    search = get_object_or_404(Search, pk=search_id)
    print(search.query)
    return render(request, 'main/result.html', {'query': search.query, 'result': search.get_result(search.query)})
