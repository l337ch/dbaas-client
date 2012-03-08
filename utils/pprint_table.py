__author__ = 'lchang'

import sys

def get_max_width(table, index):
    """Get the maximum width of the given column index"""
    #print len(table)
    print index
    return max([len(str(row[index])) for row in table])

def pprint_table(out, table):
    """Prints out a table of data, padded for alignment
    Each row must have the same number of columns. """
    col_paddings = []
    row_cnt = 0
    col_per_row = len(table[0])
    print table
    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))
    for row in table:
        row_cnt += 1
        # left col is justified left
        print >> out, str(row[0]).ljust(col_paddings[0] + 1),
        # rest of the cols are justified right
        for i in range(1, len(row)):
            col = str(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out
        if row_cnt == 1:
            print >> out, "=" * (sum(col_paddings) + (3*col_per_row))
            print >> out

table = [['status', 'name', 'created', 'instanceId', 'id'], [1, 'snap3', '2012-03-02 00:25:54', '5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85', '48faa511-bc89-4590-b3a1-23b01fee7440'], [1, 'this is a test', '2012-03-07 18:30:54', '5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85', '353bdcf3-b53a-45e3-8349-3a44c2036806'], [1, 'this is a test', '2012-03-07 18:33:00', '5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85', 'aea2ff3a-de10-43da-b317-4d01bc664ac1'], [1, 'test-snapsot', '2012-03-07 19:45:26', '5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85', 'ace94cb9-8c8d-4999-8433-d716fab5ff74']]


out = sys.stdout
pprint_table(out, table)

