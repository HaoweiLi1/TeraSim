#!/usr/bin/env bash

set -euo pipefail

BASE_DIR="/home/haowei/Documents/TeraSim/CrashCase_HD_Video"
CONVERTER_SCRIPT="/home/haowei/Documents/TeraSim/scripts/convert_terasim_to_cosmos.py"
PYTHON_BIN="${PYTHON_BIN:-python}"
STATUS_CSV="/home/haowei/Documents/TeraSim/hdvideo_status.csv"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "error: cannot find python interpreter '$PYTHON_BIN'" >&2
    exit 1
fi

if [[ ! -f "$CONVERTER_SCRIPT" ]]; then
    echo "error: converter script not found at $CONVERTER_SCRIPT" >&2
    exit 1
fi

declare -A status_map=()
declare -A note_map=()
declare -A timestamp_map=()

if [[ -f "$STATUS_CSV" ]]; then
    while IFS=',' read -r case_name status note timestamp _; do
        [[ "$case_name" == "case" ]] && continue
        [[ -z "$case_name" ]] && continue
        status_map["$case_name"]="$status"
        note_map["$case_name"]="${note:-}"
        timestamp_map["$case_name"]="${timestamp:-}"
    done < "$STATUS_CSV"
fi

shopt -s nullglob

crash_dirs=("$BASE_DIR"/*)

if [[ ${#crash_dirs[@]} -eq 0 ]]; then
    echo "warning: no crash cases found under $BASE_DIR" >&2
    exit 0
fi

for crash_dir in "${crash_dirs[@]}"; do
    [[ -d "$crash_dir" ]] || continue

    crash_name="$(basename "$crash_dir")"
    output_dir="$crash_dir/hdvideo"
    fcd_path="$crash_dir/final.fcd.xml"
    map_path="$crash_dir/map.net.xml"

    if [[ -f "$STATUS_CSV" ]] && [[ "${status_map[$crash_name]-}" == "success" ]]; then
        echo "[INFO] Skipping $crash_name (already marked success)"
        continue
    fi

    if [[ ! -f "$fcd_path" ]]; then
        echo "warning: skipping $crash_name (missing $fcd_path)" >&2
        status_map["$crash_name"]="fail"
        note_map["$crash_name"]="missing final.fcd.xml"
        timestamp_map["$crash_name"]="$(date --iso-8601=seconds)"
        continue
    fi

    if [[ ! -f "$map_path" ]]; then
        echo "warning: skipping $crash_name (missing $map_path)" >&2
        status_map["$crash_name"]="fail"
        note_map["$crash_name"]="missing map.net.xml"
        timestamp_map["$crash_name"]="$(date --iso-8601=seconds)"
        continue
    fi

    mkdir -p "$output_dir"

    echo "[INFO] Processing $crash_name"
    if "$PYTHON_BIN" "$CONVERTER_SCRIPT" \
        --path_to_output "$output_dir" \
        --path_to_fcd "$fcd_path" \
        --path_to_map "$map_path" \
        --openrouter_model google/gemini-2.5-pro \
        --streetview_retrieval; then
        status_map["$crash_name"]="success"
        note_map["$crash_name"]=""
        timestamp_map["$crash_name"]="$(date --iso-8601=seconds)"
    else
        exit_code=$?
        echo "error: $crash_name failed with exit code $exit_code" >&2
        status_map["$crash_name"]="fail"
        note_map["$crash_name"]="converter exit $exit_code"
        timestamp_map["$crash_name"]="$(date --iso-8601=seconds)"
    fi
done

tmp_csv="${STATUS_CSV}.tmp"
{
    echo "case,status,note,timestamp"
    for case_name in "${!status_map[@]}"; do
        note="${note_map[$case_name]-}"
        timestamp="${timestamp_map[$case_name]-}"
        printf '%s,%s,%s,%s\n' "$case_name" "${status_map[$case_name]}" "$note" "$timestamp"
    done | sort
} > "$tmp_csv"

mv "$tmp_csv" "$STATUS_CSV"

