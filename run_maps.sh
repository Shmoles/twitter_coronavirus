#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs logs
max_jobs=12
running=0

for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
    base=$(basename "$file")

    if [[ -f "outputs/${base}.lang" && -f "outputs/${base}.country" ]]; then
        echo "skipping $base"
        continue
    fi

    nohup python3 src/map.py \
        --input_path "$file" \
        --output_folder outputs \
        > "logs/${base}.log" 2>&1 &

    echo "started $base"
    ((running+=1))

    if (( running >= max_jobs )); then
        wait -n
        ((running-=1))
    fi
done

wait
