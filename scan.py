#!/usr/bin/python
import os
import time
import string
import fnmatch
import argparse
from core.structs.categorizer import FirstLetterSplitter
from core.btree import KeyTree
from core.ngrams import NGramIndex
from core.parsers.SGM import reuters_SGM_processor

parser = argparse.ArgumentParser(description='Scans folders for documents')
parser.add_argument('-f', '--filter')
parser.add_argument('-d', '--directory')
parser.add_argument('-o', '--output')

args = parser.parse_args()

matches = [ os.path.join(args.directory, document) for document in os.listdir(args.directory)
    if fnmatch.fnmatch(document, args.filter) ]


td = FirstLetterSplitter(KeyTree, NGramIndex(2))



start_time = time.time()
for match in matches:
    print("[*] Parsing: " + match)
    parsed_articles = reuters_SGM_processor(match)
    print("[*] Adding:  " + match)
    for parsed_article in parsed_articles:
        td.update_tree(parsed_article)


print("[+] Parsing complete")
print("[*] Time elapsed : "+str(time.time()-start_time))
#td.tree.visualizeTree()

import pickle
print("[*] Dumping tokentree")
with open("storage/" + args.output + ".pickle", 'wb') as pickle_file:
    pickle.dump(td, pickle_file)
print("[+] Dumping done")
