from django.db import models
from eldar import build_query
import re

class Document(models.Model):
    title = models.CharField(max_length=1000, null=True, default='Title')
    text = models.CharField(max_length=20000, null=True, default='Sample text')
    snippet = models.CharField(max_length=300, null=True, default='Sample text')
    url = models.CharField(max_length=1000, null=True, default='Sample text')


class Search(models.Model):
    query = models.CharField(max_length=1000, null=True, default="text")

    def get_result(self, query):
        match = re.search('[а-яА-Я]+', query)
        request = build_query(query)
        documents = Document.objects.all()
        docs_sim = {}
        snippet = ''
        for doc in documents:
            if request(doc.text):
                i = doc.text.find(match.group())
                snippet = doc.text[i-100:i] + doc.text[i:i+100] + '... читать продолжение в исочнике '
                doc.snippet = snippet
                docs_sim[doc] = 1
        return docs_sim
