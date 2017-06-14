#!/usr/bin/python
import fnmatch
from collections import defaultdict
import itertools


def get_n_grams(token, grams_count):
    grams = [token[i:i + grams_count] for i in range(len(token) - grams_count + 1)]
    grams.append(grams[-1][-grams_count + 1:] + "$")
    grams.insert(0, "$" + grams[0][:grams_count - 1])
    return grams


def query_combinations(parts):
    return list(itertools.product(*parts))


class NGramIndex:
    def __init__(self, length):
        self.length = length
        self.index = defaultdict(set)

    def index_token(self, token):
        try:
            ngrams = get_n_grams(token, self.length)
        except IndexError:
            # tokens with 1 length make this :(
            pass
        else:
            for ngram in ngrams:
                self.index[ngram].update([token])

    def token_correction(self, token):
        pass

    def get_(self, token):
        pass

    def suggestions(self, ngrams):
        if ngrams:
            results = self.index[ngrams[0]]
            # print(results)
            for ngram in range(1, len(ngrams)):
                results = results & self.index[ngrams[ngram]]
            return results
        return set()

    def wildcard_ngrams(self, wildcard_input):
        ngrams = []
        token_parts = wildcard_input.split("*")
        last_part = len(token_parts)-1

        for enum, part in enumerate(wildcard_input.split("*")):
            if part:
                part_ngrams = get_n_grams(part, self.length)

                if enum != last_part:
                    # If not the last part of the token remove the char$
                    part_ngrams.pop(-1)

                if enum != 0:
                    # If not the first part of the token remove the $char
                    part_ngrams.pop(0)

                # print(part_ngrams)

                ngrams += part_ngrams
        return ngrams

    def post_filtering(self, wildcard_input, suggestions):
        return [suggestion for suggestion in suggestions if fnmatch.fnmatch(suggestion, wildcard_input)]


if __name__ == "__main__":
    ni = NGramIndex(2)
    print(get_n_grams("results", 2))
    print(ni.wildcard_ngrams("res*lts"))
