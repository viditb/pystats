"""Contains Table class definiton
"""

import os
import csv
from record import Record


class Table(object):

    """Represents a table as a list of objects"""

    def __init__(self):
        self.records = []

    def __len__(self):
        return len(self.records)

    def ReadFile(self, data_dir, filename, fields, constructor, delim=",", n=None):
    # def ReadFile(self, data_dir, filename, delim=",", fields = [], n=None):
        """Reads a compressed data file builds one object per record.

        Args:
            data_dir: string directory name
            filename: string name of the file to read

            fields: sequence of (name, start, end, case) tuples specifying
            the fields to extract

            constructor: what kind of object to create
        """
        filename = os.path.join(data_dir, filename)

        reader = csv.reader(open(filename), delimiter=delim)

        headers = next(
            reader, None)  # returns the headers or `None` if the input is empty

        # if not fields:
        #    fields = headers

        columns = [(headers.index(
            field), field, cast) for (field, cast) in fields]

        # print columns

        for i, row in enumerate(reader):
            if i == n:
                break
            record = self.MakeRecord(row, columns, constructor)
            self.AddRecord(record)

        '''
        for i, line in enumerate(fp):
            if i == n:
                break
            record = self.MakeRecord(line, fields, constructor)
            self.AddRecord(record)
        fp.close()
        '''

    def MakeRecord(self, line, fields, constructor):
        """Scans a line and returns an object with the appropriate fields.

        Args:
            line: string line from a data file

            fields: sequence of (name, start, end, cast) tuples specifying
            the fields to extract

            constructor: callable that makes an object for the record.

        Returns:
            Record with appropriate fields.
        """
        obj = constructor()

        for (field_index, name, cast) in fields:
            try:
                s = line[field_index]
                val = cast(s)
            except ValueError:
                # print line
                # print field, start, end, s
                val = 'NA'
            setattr(obj, name, val)

        return obj

    def AddRecord(self, record):
        """Adds a record to this table.

        Args:
            record: an object of one of the record types.
        """
        self.records.append(record)

    def ExtendRecords(self, records):
        """Adds records to this table.

        Args:
            records: a sequence of record object
        """
        self.records.extend(records)

    def Recode(self):
        """Child classes can override this to recode values."""
        pass


if __name__ == '__main__':
    test_table = Table()
    test_table.ReadFile("C:\\Users\\vidit.bansal\\Desktop\\pystats", "test.csv", n=2, fields=[
                        ('Date_1', str), ('Outcome_M11', float)], constructor=Record)

    print len(test_table)
    print
    
    for record in test_table.records:
        print record.Date_1