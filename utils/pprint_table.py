__author__ = 'lchang'

import sys

class PPrintTable():

    def __init__(self, out, content):
        self.out = out
        self.content = content

    def get_max_width(self, index):
        """Get the maximum width of the given column index"""
        #print len(table)
        return max([len(str(row[index])) for row in table])

    def pprint_table(self):
        """Prints out a table of data, padded for alignment
        Each row must have the same number of columns. """
        table = self.content
        out = self.out
        col_paddings = []
        row_cnt = 0
        col_per_row = len(table[0])

        for i in range(len(table[0])):
            col_paddings.append(self.get_max_width(i))

        print "\n"

        for row in table:
            row_cnt += 1
            # left col is justified left
            print >> out, str(row[0]).ljust(col_paddings[0] + 1),
            # rest of the cols are justified right
            for i in range(1, len(row)):
                col = str(row[i]).ljust(col_paddings[i] + 2)
                print >> out, col,
            print >> out
            #print a border line under for the first header row
            if row_cnt == 1:
                print >> out, "=" * (sum(col_paddings) + (3*col_per_row))

        print >> out, "=" * (sum(col_paddings) + (3*col_per_row))



table = [['status', 'name', 'created', 'instanceId', 'id'], [1, 'snap3', '2012-03-02 00:25:54', '5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85', '48faa511-bc89-4590-b3a1-23b01fee7440'], [1, 'this is a test', '2012-03-07 18:30:54', '5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85', '353bdcf3-b53a-45e3-8349-3a44c2036806'], [1, 'this is a test', '2012-03-07 18:33:00', '5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85', 'aea2ff3a-de10-43da-b317-4d01bc664ac1'], [1, 'test-snapsot', '2012-03-07 19:45:26', '5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85', 'ace94cb9-8c8d-4999-8433-d716fab5ff74']]


out = sys.stdout

ptable = PPrintTable(out, table)
ptable.pprint_table()

