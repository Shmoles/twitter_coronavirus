#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
parser.add_argument('--output_path', default=None)
args = parser.parse_args()

import os
import re
import json
import matplotlib.pyplot as plt

with open(args.input_path, encoding='utf-8') as f:
    counts = json.load(f)

if args.key not in counts:
    raise KeyError(f'{args.key} not found in {args.input_path}')

items = []
for k, v in counts[args.key].items():
    if args.percent:
        denom = counts.get('_all', {}).get(k, 0)
        if denom == 0:
            continue
        v = v / denom
    items.append((k, v))

top10 = sorted(items, key=lambda item: (item[1], item[0]), reverse=True)[:10]
top10 = sorted(top10, key=lambda item: (item[1], item[0]))

labels = [k for k, _ in top10]
values = [v for _, v in top10]

if args.output_path is None:
    os.makedirs('plots', exist_ok=True)
    base = os.path.splitext(os.path.basename(args.input_path))[0]
    safe_key = re.sub(r'[^0-9A-Za-z가-힣ぁ-んァ-ン一-龥_-]+', '_', args.key).strip('_')
    suffix = '_percent' if args.percent else ''
    args.output_path = os.path.join('plots', f'{base}_{safe_key}{suffix}.png')

plt.figure(figsize=(12, 6))
plt.bar(labels, values)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Language or Country')
plt.ylabel('Percent' if args.percent else 'Count')
plt.title(f'{args.key} from {os.path.basename(args.input_path)}')
plt.tight_layout()
plt.savefig(args.output_path)
plt.close()

print(args.output_path)
