import re

from bs4 import BeautifulSoup
from core.parsers import parser
from core.structs.documents import document

split = re.compile('\s+', re.VERBOSE | re.MULTILINE)
escape = re.compile('(\\n|\\t|\\r)', re.VERBOSE | re.MULTILINE)


class HTMLParser(parser.PluginParser):
    name = "HTML Parser"
    handles = "*.html"

    @staticmethod
    def parse_document(file_name):
        f = open(file_name, 'r')
        page = f.read()
        # Remove unnecessary characters
        page = re.sub(escape, "", page)
        page = re.sub(split, " ", page)
        soup = BeautifulSoup(page, "html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        title = ""
        if hasattr(soup.title, 'title'):
            title = soup.title.text

        page = soup.get_text()
        page = re.sub(split, " ", page)

        f.close()
        return [document(file_name, title, page)]
