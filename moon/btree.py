#!/usr/bin/python
import math
import ast
import os
import os.path


KEY_LEN, TERM_OCCUR_LEN, DOC_DICTIONARY_LEN = 30, 10, 310
LINE_LENGTH = KEY_LEN + TERM_OCCUR_LEN + DOC_DICTIONARY_LEN
SEP_CHAR = '&^'
FILL_CHAR = '~'


class CSVBTree:
    def __init__(self, name):
        self.name = name
        self.rows = 0
        if os.path.isfile(name):
            with open(self.name, 'r') as csv_file:
                self.rows = sum([1 for _ in csv_file])

    def next_middle(self, level=1):
        return self.rows // (2 ** level)

    @staticmethod
    def row_to_csv(key, term_occurance, doc_freq_dict):
        remaining_key = (KEY_LEN - len(key) - len(SEP_CHAR)) * FILL_CHAR
        remaining_term = (TERM_OCCUR_LEN - len(str(term_occurance)) - len(SEP_CHAR)) * FILL_CHAR
        # -1 because we add newline
        remaining_dict = (DOC_DICTIONARY_LEN - len(str(doc_freq_dict)) - 1) * FILL_CHAR

        return f'{remaining_key}{key}&^{remaining_term}{term_occurance}&^{remaining_dict}{str(doc_freq_dict)}\n'

    @staticmethod
    def csv_to_row(row):
        vals = [val.strip(f'{FILL_CHAR}\n') for val in row.split(SEP_CHAR)]
        if len(vals) != 3:
            return None, None, None
        key, occurance, doc_freq_dict = vals
        return key, int(occurance), ast.literal_eval(doc_freq_dict)

    def init_csv(self, key, term_occurrences, value, doc_freq):
        with open(self.name, 'w') as csv_file:
            csv_file.write(
                CSVBTree.row_to_csv(key, term_occurrences, {value: doc_freq}))

    # TODO: multiple adds, finds
    def add(self, key, term_occurrences, value, doc_freq):
        if not os.path.isfile(self.name):
            self.init_csv(key, term_occurrences, value, doc_freq)
            return

        row_id, found, data = self.b_search_row(key)

        with open(f"{self.name}.lock", 'w+') as csv_file_lock:
            with open(self.name, 'r') as csv_file:
                for line_id, line in enumerate(csv_file):

                    if line_id == row_id and found:
                        _key, _term_occur, _doc_freq = CSVBTree.csv_to_row(line)
                        _term_occur += term_occurrences
                        _doc_freq[value] = doc_freq
                        csv_file_lock.write(CSVBTree.row_to_csv(_key, _term_occur, _doc_freq))

                    else:

                        if line_id == row_id and not found:
                            line_key, *_ = CSVBTree.csv_to_row(line)

                            if key < line_key:
                                csv_file_lock.write(
                                    CSVBTree.row_to_csv(key, term_occurrences, {value: doc_freq}))
                                csv_file_lock.write(line)
                                self.rows += 1
                            else:
                                csv_file_lock.write(line)
                                csv_file_lock.write(
                                    CSVBTree.row_to_csv(key, term_occurrences, {value: doc_freq}))
                                self.rows += 1

                        else:
                            csv_file_lock.write(line)

        os.remove(self.name)
        os.rename(f"{self.name}.lock", self.name)

    def find(self, key):  # TODO gets double searched for some reason
        key, found, data = self.b_search_row(key)
        if found:
            row = CSVRow(*data)
            return row, row.idf(self.rows)

        return None, 0

    def b_search_row(self, key):

        with open(self.name, 'r') as csv_file:
            lower = 0
            upper = self.rows
            row_id = 0

            while lower < upper:
                row_id = lower + (upper - lower) // 2

                seek_point = row_id * LINE_LENGTH
                csv_file.seek(seek_point)
                r = csv_file.readline()
                if len(r) < 2:
                    r = csv_file.readline()
                row_key, *data = CSVBTree.csv_to_row(r)
                # print(row_id, direction, iteration, seek_point, row_key)
                if row_key is None:
                    return row_id, False, None
                if key == row_key:
                    return row_id, True, (row_key, *data)
                elif key > row_key:
                    if lower == row_id:  # these two are the actual lines
                        return lower+1, False, None
                    lower = row_id
                elif key < row_key:
                    upper = row_id

            return row_id, False, None


class CSVRow:
    def __init__(self, key, freq, docs):
        self.key = key
        self.freq = freq
        self.documents = docs

    def idf(self, number_of_tokens):
        """
        returns the idf log(N/(1+frequency))
        :param number_of_tokens:
        :return:
        """
        return math.log(number_of_tokens / (1 + self.freq))

    def get_value(self):
        """
        returns the document identifiers where this word was found.
        :return: set
        """
        return set(self.documents.keys())
