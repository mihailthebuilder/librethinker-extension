#!/usr/bin/env bash
#
# Build the .oxt bundle and publish it as a GitHub release.
#
# The release tag and title are taken from the <version> in
# extension/description.xml (e.g. 0.2.15 -> tag "0.2.15"). The tag is created
# on the current commit, so make sure the version bump is committed and pushed
# (the release is cut from origin) before running this.
#
# Usage:
#   scripts/release.sh                 # title defaults to the version
#   scripts/release.sh "Release title" # custom release title
#
# Requires: make, gh (authenticated via `gh auth login`).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DESC="extension/description.xml"
BUNDLE="dist/LibreThinker.oxt"

# --- read version from description.xml: <version value="0.2.15" /> ---
VERSION="$(sed -n 's/.*<version value="\([^"]*\)".*/\1/p' "$DESC")"
if [ -z "$VERSION" ]; then
  echo "ERROR: could not read version from $DESC" >&2
  exit 1
fi

TITLE="${1:-$VERSION}"
echo "Version: $VERSION"

# --- refuse to clobber an existing release ---
if gh release view "$VERSION" >/dev/null 2>&1; then
  echo "ERROR: release $VERSION already exists on GitHub" >&2
  exit 1
fi

# --- build the bundle ---
echo "Building bundle..."
make unodit-zip

if [ ! -f "$BUNDLE" ]; then
  echo "ERROR: bundle not found at $BUNDLE" >&2
  exit 1
fi

# --- create the release (creates the tag on the current commit) + upload ---
echo "Creating GitHub release $VERSION..."
gh release create "$VERSION" "$BUNDLE" \
  --title "$TITLE" \
  --target "$(git rev-parse HEAD)" \
  --generate-notes

echo "Done: published release $VERSION with $BUNDLE"
