#!/usr/bin/python
import sys
import gc
import re
import pickle
import heapq
import asyncio
import operator
from core.btree import KeyTree
from core.queries.porter import PorterStemmer
from core.parsers.SGM import reuters_SGM_processor
from core.queries.querying import simple_search
from core.structs.categorizer import FirstLetterSplitter
from core.ngrams import query_combinations, NGramIndex

try:
    with open("storage/tokentree.pickle", 'rb') as pickle_file:
        print("[*] Loading pickle file")
        td = pickle.load(pickle_file)
except IOError:
    print("[-] Creating a new inverted index")
    td = FirstLetterSplitter(KeyTree, NGramIndex(2))


pts = PorterStemmer()
print("[*] Type :help to show the help screen")

while True:
    original_query = input("# ").lower()

    query = [part for part in re.split('\s+', original_query) if part]
    # print(query)
    try:
        if original_query[0] != ":":
            if "*" in original_query:
                # suggestions time yay:
                parts = []
                for token in query:
                    if "*" in token:
                        wn = td.ngram_index.wildcard_ngrams(token)
                        unfiltered_results = td.ngram_index.suggestions(wn)
                        filtered_results = td.ngram_index.post_filtering(token, unfiltered_results)
                        print(filtered_results)
                        parts.append(filtered_results)
                    else:
                        parts.append([token])

                queries = query_combinations(parts)
                simple_search(pts, td, queries, multi_query_mode=True)

            else:
                simple_search(pts, td, query)

        elif query[0] == ":suggest":
            parts = []
            for token in query[1:]:
                if "*" in token:
                    wn = td.ngram_index.wildcard_ngrams(token)
                    unfiltered_results = td.ngram_index.suggestions(wn)
                    filtered_results = td.ngram_index.post_filtering(token, unfiltered_results)
                    # print(filtered_results)
                    parts.append(filtered_results)
                else:
                    parts.append([token])

            queries = query_combinations(parts)
            for query in queries:

                print("[*] "+" ".join(query))

        elif query[0] == ":help":
            print("[*] :load [file path]")
            print("[*] Loads a file into the current btree")
            print("[*] :index save [filename]")
            print("[*] Saves the current btree in the specified filename")
            print("[*] :index load [filename]")
            print("[*] Loads the btree from the specified filename")
            print("[*] :freq [number]")
            print("[*] Shows the [number] most frequent tokens.")
            print("[*] :size")
            print("[*] Shows the size of the btrees")
            print("[*] :debug")
            print("[*] Shows information from sys._debugmallocstats()")
            print("[*] :exit")
            print("[*] Exits the application")

        elif query[0] == ":load":
            match = original_query.replace(":load ", "")
            print("[*] Parsing: " + match)
            # TODO: optimize parsing maybe
            parsed_articles = reuters_SGM_processor(match)
            print("[*] Adding:  " + match)
            for parsed_article in parsed_articles:
                td.update_tree(parsed_article)

        elif query[0] == ":test":
            print(td["a"].root.left)
            print(td["a"].root.right)

        elif query[0] == ":index":

            if query[1] == "save":
                tokentree_pickle = "tokentree.pickle"
                if len(query) > 2:
                    tokentree_pickle = query[2]

                print("[*] Dumping tokentree")
                with open("storage/" + tokentree_pickle, 'wb') as pickle_file:
                    pickle.dump(td, pickle_file)
                print("[+] Dumping done")
            elif query[1] == "load":
                tokentree_pickle = "tokentree.pickle"
                if len(query) > 2:
                    tokentree_pickle = query[2]
                print("[*] Loading tokentree")
                try:
                    with open("storage/" + tokentree_pickle, 'rb') as pickle_file:
                        td = pickle.load(pickle_file)
                except IOError:
                    print("[-] Failed to load tokentree.")
                else:
                    print("[+] Tokentree loaded.")

            elif query[1] == "unload":
                td = None

        elif query[0] == ":size":
            print("[*] Current number of ids: " + str(td.identifier.current_id))
            if len(query) > 1:
                print("[*] Size of " + query[1] + ": " + str(td.size(query[1])))
                # print("[*] Memory of " + query[1] + ": " + str(td.tree.memory(query[1])))
            else:
                print("[*] Size: " + str(td.size()))
                # print("[*] Memory: " + str(td.tree.memory()))

        elif query[0] == ":debug":
            gc.collect()
            sys._debugmallocstats()

        elif query[0] == ":freq":
            nodes = td.traverse()
            limit = int(query[1])
            for result in heapq.nlargest(limit, nodes, key=operator.itemgetter(1)):
                print("[*] " + result[0] + " : " + str(result[1]))

        elif query[0] == ":exit":
            sys.exit(0)
    except Exception as exc:
        print("[-] Bad query.")
        print("[-] Error:")
        print(exc)

