#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True)
parser.add_argument('--output_path', required=True)
args = parser.parse_args()

import json
from collections import Counter, defaultdict

total = defaultdict(Counter)

for path in args.input_paths:
    with open(path, encoding='utf-8') as f:
        tmp = json.load(f)
    for k, v in tmp.items():
        total[k].update(v)

with open(args.output_path, 'w', encoding='utf-8') as f:
    json.dump(total, f)
