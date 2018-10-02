from moon.btree import CSVBTree, SEP_CHAR, LINE_LENGTH, FILL_CHAR

csv_b_tree = CSVBTree('xd.csv', 20)
csv_val = CSVBTree.row_to_csv("xd", 5, {"4": "0.6"})
print(csv_val)

vals = CSVBTree.csv_to_row(csv_val)
print(vals)