#!/usr/bin/python
import argparse
import fnmatch
import os
import pickle
import time

from core.btree import KeyTree
from core.ngrams import NGramIndex
from core.parsers.parser import PluginsSeeker
from core.structs.categorizer import FirstLetterSplitter

parser = argparse.ArgumentParser(description='Scans folders for documents')
parser.add_argument('-f', '--filter', required=True)
parser.add_argument('-d', '--directory', required=True)
parser.add_argument('-o', '--output', required=True)

args = parser.parse_args()

matches = [os.path.join(args.directory, document) for document in os.listdir(args.directory)
    if fnmatch.fnmatch(document, args.filter)]

td = FirstLetterSplitter(KeyTree, NGramIndex(2))
PluginsSeeker.load_core_plugins()

start_time = time.time()
for match in matches:
    print("[*] Parsing: " + match)
    handler = PluginsSeeker.find_handler(match)
    parsed_articles = handler.parse_document(match)
    print("[*] Adding:  " + match)
    for parsed_article in parsed_articles:
        td.update_tree(parsed_article)

print("[+] Parsing complete")
print("[*] Time elapsed : "+str(time.time()-start_time))

print("[*] Dumping tokentree")
with open("storage/" + args.output + ".pickle", 'wb') as pickle_file:
    pickle.dump(td, pickle_file)
print("[+] Dumping done")
