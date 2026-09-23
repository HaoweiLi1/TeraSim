# TeraSim: inner snapshot, 2026-09-23

Base commit: `9e5a0e008b620ec3b5977fb0bbd33c0e4b3060bf`. Snapshot branch: `archive/20260923-inner`.

This archival branch preserves the selected source checkout as found. It does not merge changes into main or overwrite either original checkout. The companion outer/inner archive branch keeps the other version separately. Every selected source file is byte-identical to the manifest SHA-256; existing tracked deletions are recorded explicitly.

The selected case files are stored as ordinary Git blobs.

Selected cases: crash_2023174894 preserves the differing report/final FCD/BEV video and their supporting map and trajectory inputs; crash_2023197392 preserves the default HD-map converter example inputs and compact results. Shared maps, intermediate FCDs, vehicle routes and configuration are included.

Excluded: .env and credentials; API response cache/; Python caches and egg-info; rebuildable Cython .c/.so products; other cases retained unchanged in TeraSim-Agent/TeraSim; render frame sequences, multiview intermediates, processing logs, preview.png. This is a scoped Git preservation snapshot, not an archive of every generated file.
