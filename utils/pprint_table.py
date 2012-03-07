__author__ = 'lchang'

import sys

def get_max_width(table, index):
    """Get the maximum width of the given column index"""
    return max([len(str(row[index])) for row in table])

def pprint_table(out, table):
    """Prints out a table of data, padded for alignment
    Each row must have the same number of columns. """
    col_paddings = []
    row_cnt = 0
    col_per_row = len(table[0])
    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        row_cnt += 1
        # left col is justified left
        print >> out, row[0].ljust(col_paddings[0] + 1),
        # rest of the cols are justified right
        for i in range(1, len(row)):
            col = str(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out
        if row_cnt == 1:
            print >> out, "=" * (sum(col_paddings) + (3*col_per_row))

table = [['instance_id', 'instance_name', 'hostname', 'launchtime', 'status'],
    ['testid_1', 'testname_1', 'hostname_1', '2012-01-01T00:00:00-08:00', 'running']]

out = sys.stdout
pprint_table(out, table)

