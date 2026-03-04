#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--output_folder', default='outputs')
args = parser.parse_args()

import os
import zipfile
import datetime
import json
from collections import Counter, defaultdict

hashtags_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hashtags')
with open(hashtags_path, encoding='utf-8') as f:
    hashtags = [token.strip().lower() for token in f.read().split() if token.strip()]

counter_lang = defaultdict(Counter)
counter_country = defaultdict(Counter)

with zipfile.ZipFile(args.input_path) as archive:
    for filename in archive.namelist():
        print(datetime.datetime.now(), args.input_path, filename)
        with archive.open(filename) as f:
            for line in f:
                try:
                    tweet = json.loads(line)
                except Exception:
                    continue

                text = str(tweet.get('text', '')).lower()
                lang = tweet.get('lang') or 'unknown'

                place = tweet.get('place')
                country = 'UNK'
                if isinstance(place, dict):
                    country = place.get('country_code') or 'UNK'

                for hashtag in hashtags:
                    if hashtag in text:
                        counter_lang[hashtag][lang] += 1
                        counter_lang['_all'][lang] += 1
                        counter_country[hashtag][country] += 1
                        counter_country['_all'][country] += 1

os.makedirs(args.output_folder, exist_ok=True)

output_base = os.path.join(args.output_folder, os.path.basename(args.input_path))
output_lang = output_base + '.lang'
output_country = output_base + '.country'

print('saving', output_lang)
with open(output_lang, 'w', encoding='utf-8') as f:
    json.dump(counter_lang, f)

print('saving', output_country)
with open(output_country, 'w', encoding='utf-8') as f:
    json.dump(counter_country, f)
