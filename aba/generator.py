"""
aba.generator
~~~~~~~~~~~~~
"""
from __future__ import absolute_import

from .records import *


class AbaFile(object):
    """Stores ABA records and generates a complete file."""

    def __init__(self, header):
        self.header = header
        self.records = []

    @property
    def total_debit(self):
        return self._calculate_total_debit()

    @property
    def total_credit(self):
        return self._calculate_total_credit()

    @property
    def count(self):
        return len(records)

    def _calculate_total_debit(self):
        result = 0
        for record in self.records:
            if int(record.fields[4].value) == 13:
                result += int(record.fields[5].value)
        return result

    def _calculate_total_credit(self):
        result = 0
        for record in self.records:
            if int(record.fields[4].value) in (50, 53):
                result += int(record.fields[5].value)
        return result

    def add_record(self, record):
        self.records.append(record)

    def render_to_string(self, line_ending='\r\n'):
        output = self.header.render_to_string() + line_ending

        for record in self.records:
            output += record.render_to_string() + line_ending

        total = TotalRecord(
            total_credit=self.total_credit,
            total_debit=self.total_debit,
            count=self.count
        )
        output += total.render_to_string()

        return output