#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from core.ngrams import query_combinations
from core.queries.querying import simple_search
import re

class ScarletHandler(BaseHTTPRequestHandler):
    """
    Code from my spatial data project
    https://github.com/gph03n1x/Rend
    """
    def __init__(self, *args, **kwargs):
        super(ScarletHandler, self).__init__(*args, **kwargs)

    def _set_headers(self):
        """
        Sends 200 response and html content headers
        :return:
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
        Sends the .ico image and handle the action request in
        the get request.
        :return:
        """
        self._set_headers()

        if self.path.endswith("/"):
            self.path = self.path[:-1]

        self.display_query_form()


    def do_POST(self):
        request_headers = self.headers

        content_length = request_headers.get_all("content-length")

        length = int(content_length[0]) if content_length else 0

        original_query = str(self.rfile.read(length))[8:-1] # removes b'query= and the trailing '
        # TODO: ['hurricane+%3Aand%3A+sugar'] should be hurricane :and: sugar

        print(original_query)

        query = [part for part in re.split('\s+', original_query) if part]
        if "*" in original_query:
            parts = []
            for token in query:
                if "*" in token:
                    wn = self.server.td.ngram_index.wildcard_ngrams(token)
                    unfiltered_results = self.server.td.ngram_index.suggestions(wn)
                    filtered_results = self.server.td.ngram_index.post_filtering(token, unfiltered_results)
                    print(filtered_results)
                    parts.append(filtered_results)
                else:
                    parts.append([token])
            queries = query_combinations(parts)
            results = simple_search(self.server.pts, self.server.td, queries, multi_query_mode=True, use_terminal = False)

        else:
            print(query)
            results = simple_search(self.server.pts, self.server.td, query, use_terminal = False)

        self._set_headers()
        self.wfile.write(str(results).encode())

    def display_query_form(self):
        self.wfile.write("""
                <html>
                    <body>
                        <form method="post">
                            <input name='query' />
                            <input type='submit' />
                        </form>
                    </body>
                </html>
                """.encode())



def make_http_server(token_tree, pts, port, server_class=HTTPServer):
    """
    Creates and httpd server daemon and returns it.
    :param spatial_index:
    :param port:
    :param server_class:
    :return:
    """
    server_address = ('', port)
    httpd = server_class(server_address, ScarletHandler)
    httpd.td= token_tree
    httpd.pts = pts
    httpd.allowed_actions = ["query", "suggest", "frequency", "size"]
    return httpd
