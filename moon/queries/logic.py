#!/usr/bin/python


def intersect(a, b):
    """
    returns common items between two sets
    """
    if a is None or b is None:
        return set()
    return set(a & b)


def union(a, b):
    """
    returns the sum of both lists without duplicates
    """
    if a is None:
        return b
    if b is None:
        return a
    return set(a | b)

def exempt(a, b):
    """
    exempts b from a
    """
    if a is None:
        return set()
    if b is None:
        return a
    return set(a) - set(b)
