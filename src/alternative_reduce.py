#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True)
parser.add_argument('--input_glob', default='outputs/geoTwitter20-*.zip.lang')
parser.add_argument('--output_path', default='plots/hashtag_timeseries.png')
args = parser.parse_args()

import os
import glob
import json
import datetime
import matplotlib.pyplot as plt

series = {hashtag: [] for hashtag in args.hashtags}
dates = []

for path in sorted(glob.glob(args.input_glob)):
    name = os.path.basename(path)
    date_text = name.replace('geoTwitter', '').replace('.zip.lang', '')
    date_obj = datetime.datetime.strptime(date_text, '%y-%m-%d').date()
    dates.append(date_obj)

    with open(path, encoding='utf-8') as f:
        counts = json.load(f)

    for hashtag in args.hashtags:
        total = sum(counts.get(hashtag, {}).values())
        series[hashtag].append(total)

os.makedirs(os.path.dirname(args.output_path) or '.', exist_ok=True)

plt.figure(figsize=(14, 7))
for hashtag in args.hashtags:
    plt.plot(dates, series[hashtag], label=hashtag)

plt.xlabel('Day of year')
plt.ylabel('Tweet count')
plt.title('Hashtag usage over time in 2020')
plt.legend()
plt.tight_layout()
plt.savefig(args.output_path)
plt.close()

print(args.output_path)
