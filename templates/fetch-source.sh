#!/usr/bin/env bash
# Source-only tasks: reproduce the exact tree the participant investigates.
#
# Askable packages this into whatever the evaluation harness needs. Your job is
# to make the tree reproducible and to prove it, which is what the checksum does.
set -euo pipefail

REPO_URL="https://github.com/OWNER/REPO.git"
COMMIT="FULL_40_CHARACTER_SHA"
DEST="${1:-./source}"

rm -rf "$DEST"
git clone --no-checkout "$REPO_URL" "$DEST"
git -C "$DEST" checkout --detach "$COMMIT"
rm -rf "$DEST/.git"

# Retain an archive and record its SHA-256 in
# task.json → environment.source_acquisition.archive_sha256, so the tree can be
# verified without network access later.
tar --sort=name --mtime="UTC 1970-01-01" --owner=0 --group=0 --numeric-owner \
    -czf source.tar.gz -C "$(dirname "$DEST")" "$(basename "$DEST")"
shasum -a 256 source.tar.gz
