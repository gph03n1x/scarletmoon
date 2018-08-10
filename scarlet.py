#!/usr/bin/python
import heapq
import json
import operator
import pickle
import re
import sys
import time

from nameko.timer import timer
from nameko.web.handlers import http
from werkzeug.wrappers import Response

from moon.ngrams import query_combinations, suggest_if_needed
from moon.plugins import PluginsSeeker
from moon.queries.querying import simple_search
from moon.structs.categorizer import NamedIndexes
from moon.tokens import ExtendedPorterStemmer

STORAGE = "storage/tokentree.pickle"


pts = ExtendedPorterStemmer()
PluginsSeeker.load_core_plugins('parsers')
PluginsSeeker.load_core_plugins('query')

STATS_LIMIT = 100
SAVE_INTERVAL = 60

try:
    with open(STORAGE, 'rb') as pickle_file:
        print("[*] Loading pickle file")
        td = pickle.load(pickle_file)
except IOError:
    td = NamedIndexes()


class Service:
    name = 'scarlet'

    @http('GET', "/search")
    @http('GET', "/")
    def text_search(self, request):
        original_query = request.args.get('query')
        index_name = request.args.get('name')
        if not original_query:
            return "form boi"
        start = time.clock()
        result = self.get_results(index_name, original_query)

        return Response(json.dumps({"results": result, "time": time.clock() - start}),
                        status=200, mimetype='application/json')

    @http('GET', "/stats")
    def scarlet_stats(self, request):
        index_name = request.args.get('name')
        result = self.get_stats(index_name)
        return Response(json.dumps(result), status=200, mimetype='application/json')


    @http('POST', "/index")
    def index_data(self, request):
        print(request.data)
        match = request.get_json().get('filename')
        url = request.get_json().get('origin_url')
        index_name = request.get_json().get('name')

        self.add_to_index(index_name, match, url)
        return Response(json.dumps({"status": 200}))


    @http('GET', "/suggest")
    def suggest_corrections(self, request):
        index_name = request.args.get('name')
        original_query = request.args.get('query').lower()
        result = self.get_suggestions(index_name, original_query)
        return Response(json.dumps(result), status=200, mimetype='application/json')

    @timer(interval=SAVE_INTERVAL)
    def overwrite_token_tree(self):
        # TODO save only if changed.
        print("[*] Saving token tree")
        with open(STORAGE, 'wb') as pickle_file:
            pickle.dump(td, pickle_file)
        print("[+] Saved token tree")

    def add_to_index(self, index, match, url):
        print("[*] Parsing: " + match)
        handler = PluginsSeeker.find_appropriate_parser(match)
        parsed_articles = handler.parse_document(match)
        print("[*] Adding:  " + match)
        for parsed_article in parsed_articles:
            td[index].update_tree(parsed_article, url)

    def get_results(self, index, original_query):
        original_query = PluginsSeeker.process_query(original_query)
        print(original_query)
        query = [suggest_if_needed(td[index], part) for part in re.split('\s+', original_query.lower()) if part]

        if "*" in original_query:
            queries = query_combinations(query)
            result = simple_search(pts, td[index], queries)

        else:
            result = simple_search(pts, td[index], [query])
        return result

    def get_stats(self, index):
        limit = max(STATS_LIMIT, td[index].size())
        nodes = td[index].traverse()
        json_response = {
            "top_frequencies": [
                [result[0], result[1]] for result in heapq.nlargest(limit, nodes, key=operator.itemgetter(1))
            ],
            "size": td[index].size(),  # TODO might be bugged
            "limit": limit

        }
        return json_response

    def get_suggestions(self, index, original_query):
        query = [suggest_if_needed(td[index], part) for part in re.split('\s+', original_query) if part]
        queries = query_combinations(query)
        return [" ".join(query) for query in queries]
