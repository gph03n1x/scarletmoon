#!/usr/bin/python
import argparse
import fnmatch
import os
import shutil
import time


from moon.plugins import PluginsSeeker
from moon.structs.categorizer import NamedIndexes
from scarlet import STORAGE_ID

parser = argparse.ArgumentParser(description='Scans folders for documents')
parser.add_argument('-f', '--filter', required=True)
parser.add_argument('-d', '--directory', required=True)

args = parser.parse_args()
# TODO debug flag
# shutil.rmtree('storage/')
# os.mkdir('storage/')

matches = [os.path.join(args.directory, document) for document in os.listdir(args.directory)
    if fnmatch.fnmatch(document, args.filter)]

td = NamedIndexes(STORAGE_ID)
PluginsSeeker.load_core_plugins('parsers')
PluginsSeeker.load_core_plugins('query')

start_time = time.time()
for match in matches:
    print("[*] Parsing: " + match)
    handler = PluginsSeeker.find_appropriate_parser(match)
    parsed_articles = handler.parse_document(match)
    print("[*] Adding:  " + match)
    for parsed_article in parsed_articles:
        td['reuters'].update_tree(parsed_article)

print("[+] Parsing complete")
print("[*] Time elapsed : "+str(time.time()-start_time))
