#!/usr/bin/env python3

"""A script to generate a submission csv file from the materials schema.
A couple of columns have special behaviour (e.g. HMDMC and taxon id).
The rest are procedural, either alternating specific values
from an "allowed" field (e.g. "male", "female" for the
"gender" column), or simply counting (e.g. "s0", "s1",
"s2", etc. for the "supplier name" column).
It is considered a bug in the materials service if the 
friendly name given for the column does not match the
"field_name_regex" for the same column."""

import sys

if sys.version_info.major < 3:
    exit("This is a Python 3 script. It will not work with Python %s."%
             sys.version_info.major)

import json
import urllib.request
import csv

try:
    import ssl
except ImportError:
    ssl = None


SKIP_KEYS = {'scientific_name'}
DEFAULT_URL = 'https://wip.aker.sanger.ac.uk/material_service/materials/schema'

class WellPosColumn:
    def __init__(self, num_rows, num_cols):
        self.heading = 'Well Position'
        self.num_rows = num_rows
        self.num_cols = num_cols
    def __call__(self, index):
        x,y = divmod(index, self.num_rows)
        return '%s:%s'%(chr(ord('A')+y), x+1)

class EnumeratingColumn:
    def __init__(self, heading, values):
        self.heading = heading
        self.values = values
        self.scale = 1
    def __call__(self, index):
        if self.scale > 1:
            index //= self.scale
        return self.values[index%len(self.values)]

class CountingColumn:
    def __init__(self, heading, text):
        self.heading = heading
        self.text = text
        self.num_length = 0
    def __call__(self, index):
        num = str(index)
        if self.num_length:
            num = num.rjust(self.num_length, '0')
        return self.text + num

def hmdmc_column(index):
    return '18/0001'

hmdmc_column.heading = 'HMDMC'

def taxon_column(index):
    return 9606

taxon_column.heading = 'Taxon ID'

def make_column(key, prop):
    heading = prop['friendly_name'].rstrip('?')
    if prop.get('hmdmc_format'):
        return hmdmc_column
    if key=='taxon_id':
        return taxon_column
    values = prop.get('allowed')
    if values:
        return EnumeratingColumn(heading, values[:2])
    return CountingColumn(heading, heading[0])
    
def make_columns(keys, props, num_rows, num_cols):
    columns = [WellPosColumn(num_rows, num_cols)]
    for key in keys:
        if key not in SKIP_KEYS:
            columns.append(make_column(key, props[key]))
    scale = 1
    num_length = len(str(num_rows*num_cols-1))
    for column in columns:
        if isinstance(column, EnumeratingColumn):
            column.scale = scale
            scale += 1
        elif isinstance(column, CountingColumn):
            column.num_length = num_length
    return columns

# -----
# getting the schema
# -----

def make_opener():
    handlers = [urllib.request.ProxyHandler({})]
    if ssl:
        ctxt = ssl.SSLContext()
        ctxt.verify_mode = ssl.CERT_NONE
        handlers.append(urllib.request.HTTPSHandler(context=ctxt))
    return urllib.request.build_opener(*handlers)

def read_json(url):
    with make_opener().open(url) as fin:
        return json.load(fin)

# -----
# main functions
# -----

def run(url, num_rows, num_cols, fout):
    schema = read_json(url)
    keys = schema['show_on_form']
    props = schema['properties']
    columns = make_columns(keys, props, num_rows, num_cols)
    wr = csv.writer(fout)
    wr.writerow(column.heading for column in columns)
    for i in range(num_rows*num_cols):
        wr.writerow(column(i) for column in columns)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', '-u', help="url of schema",
                        default=DEFAULT_URL)
    parser.add_argument('--output', '-o', metavar='PATH',
                            help="output to file")
    parser.add_argument('--rows', type=int, default=8,
                        help="num of rows in plate (default 8)")
    parser.add_argument('--columns', type=int, default=12,
                        help="num of columns in plate (default 12)")
    args = parser.parse_args()
    if args.output:
        with open(args.output, 'w') as fout:
            run(args.url, args.rows, args.columns, fout)
    else:
        run(args.url, args.rows, args.columns, sys.stdout)
