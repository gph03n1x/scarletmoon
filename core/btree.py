#!/usr/bin/python
import math


class KeyNode:
    def __init__(self, key, value, term_freq):
        self.left = None
        self.right = None
        self.key = key
        self.freq = 1
        self.documents = {value: term_freq}

    def get_value(self):
        return set(self.documents.keys())

    def update(self, value, frequency):
        self.freq += 1
        self.documents[value] = frequency

    def idf(self, number_of_tokens):
        return math.log(number_of_tokens / (1 + self.freq))

    def __str__(self):
        return "Node(key={0})".format(self.key)

    def __repr__(self):
        return str(self)


class KeyTree:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = None
        self.size = 0

    def get_doc_count(self):
        if self.parent is None:
            return self.size
        return self.parent.count

    def add(self, key, value, frequency):
        if self.root is None:
            self.root = KeyNode(key, value, frequency)
            self.size += 1
            return
        node = self.root
        while True:
            if key < node.key:
                if node.left is not None:
                    node = node.left
                    continue
                else:
                    node.left = KeyNode(key, value, frequency)
                    self.size += 1
                    break

            elif node.key == key:
                node.update(value, frequency)
                break
            else:
                if node.right is not None:
                    node = node.right
                    continue

                else:
                    node.right = KeyNode(key, value, frequency)
                    self.size += 1
                    break

    def find(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return node, node.idf(self.get_doc_count())
            elif key < node.key and node.left is not None:
                node = node.left
                continue
            elif key > node.key and node.right is not None:
                node = node.right
                continue
            else:
                break
        return None

    def delete_tr(self):
        # garbage collector will do this for us.
        self.root = None

    def traverse(self):
        queue = [self.root]
        nodes = []
        while queue:
            node = queue.pop()
            nodes.append((node.key, node.freq))
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return nodes

    def visualize_tree(self, key):
        # TODO: Improve visualization
        if self.root is not None:
            thislevel = [self.root]
            a = '                                                             '
            f = open("debug/output-" + key + ".txt", "w")
            while thislevel:
                nextlevel = []
                # print(len(a)/2)
                a = a[:int(len(a)/2)]
                for n in thislevel:
                    f.write(a + ' ' + str(n))
                    if n.left:
                        nextlevel.append(n.left)
                    if n.right:
                        nextlevel.append(n.right)

                thislevel = nextlevel
                f.write("\n")
