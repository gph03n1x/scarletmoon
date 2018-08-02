#!/usr/bin/python
import re

tokenizer_regex = re.compile('[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+',
                             re.MULTILINE)


def tokenizer(text):
    """
    Tokenizes text into tokens.
    :param text:
    :return:
    """
    tokens = tokenizer_regex.findall(text)
    # filter(lambda s: len(s)>1, tokens)
    return tokens


if __name__ == "__main__":
    t = """Question: I want try - something.  Should I?
    Answer  : I'd assume so.  Give it a try.
    Aren't you in hurry ?"""
    tk = tokenizer(t)
    print(tk)
    """
    ['Question', 'I', 'want', 'try', 'something', 'Should', 'I', 'Answer', "I'd",
    'assume', 'so', 'Give', 'it', 'a', 'try', "Aren't", 'you', 'in', 'hurry']
    """
