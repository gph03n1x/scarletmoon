#!/usr/bin/python
from bs4 import BeautifulSoup
from core.structs.documents import document


def reuters_SGM_processor(file_name):
    def parse(article):
        title = ""
        body = ""
        content = article.find('text')
        _title = content.title
        if _title is not None:
            title = _title.string

        _body = content.body
        if _body is not None:
            body = _body.string

        return str(title), str(body)

    f = open(file_name, 'r')
    articles = BeautifulSoup(f.read(), 'html.parser').findAll('reuters')
    f.close()
    return [document(file_name, *parse(article)) for article in articles]
