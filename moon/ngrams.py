#!/usr/bin/python
import fnmatch
import itertools
from collections import defaultdict


def get_n_grams(token, grams_count):
    """
    returns the n_grams of a token
    :param token: ex. results
    :param grams_count: ex. 2
    :return: ['$r', 're', 'es', 'su', 'ul', 'lt', 'ts', 's$']
    """
    grams = [token[i:i + grams_count] for i in range(len(token) - grams_count + 1)]
    grams.append(grams[-1][-grams_count + 1:] + "$")
    grams.insert(0, "$" + grams[0][:grams_count - 1])
    return grams


def query_combinations(parts):
    """
    creates a combination of all the possible queries
    that could come out of wildcard query
    :param parts:
    :return:
    """
    return list(itertools.product(*parts))


class NGramIndex:
    def __init__(self, length):
        self.length = length
        self.index = defaultdict(set)

    def index_token(self, token):
        """
        creates an index with the n_grams of each token.
        :param token:
        :return:
        """
        try:
            n_grams = get_n_grams(token, self.length)
        except IndexError:
            # tokens with 1 length make this :(
            pass
        else:
            for n_gram in n_grams:
                self.index[n_gram].update([token])

    def suggestions(self, wildcard_input):
        """
        gets all the common tokens from an n_gram list.
        :param wildcard_input:
        :return:
        """
        n_grams = self.wildcard_n_grams(wildcard_input)
        if n_grams:
            results = self.index[n_grams[0]]
            # print(results)
            for n_gram in range(1, len(n_grams)):
                results = results & self.index[n_grams[n_gram]]

            return NGramIndex.post_filtering(wildcard_input, results)

        return set()

    def wildcard_n_grams(self, wildcard_input):
        """
        creates the n_grams that based on the wildcard input.
        :param wildcard_input:
        :return:
        """
        n_grams = []
        token_parts = wildcard_input.split("*")
        last_part = len(token_parts)-1

        for enum, part in enumerate(wildcard_input.split("*")):
            if part and len(part) >= self.length:

                part_n_grams = get_n_grams(part, self.length)

                if enum != last_part:
                    # If not the last part of the token remove the char$
                    part_n_grams.pop(-1)

                if enum != 0:
                    # If not the first part of the token remove the $char
                    part_n_grams.pop(0)

                n_grams += part_n_grams
        return n_grams

    @staticmethod
    def post_filtering(wildcard_input, suggestions):
        """
        checks if the suggestion actually matches the wildcard query
        :param wildcard_input:
        :param suggestions:
        :return:
        """
        return [suggestion for suggestion in suggestions if fnmatch.fnmatch(suggestion, wildcard_input)]


def suggest_if_needed(td, token):
    if "*" in token:
        return td.ngram_index.suggestions(token)
    return token


if __name__ == "__main__":
    ni = NGramIndex(2)
    print(get_n_grams("results", 2))
    print(ni.wildcard_n_grams("res*lts"))
