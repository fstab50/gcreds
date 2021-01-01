#!/usr/bin/env bash

#
#   - Summary:   Post commit hook, updates version throughout project
#   - Location:  .git/hooks
#   - Filename:  commit-msg
#

source core/version.py

VERSION="$__version__"
DEPRECATED="$(grep 'Version:' README.md | awk -F ':' '{print $2}')"

if [ ! "$DEPRECATED" ]; then
    # attempt with markdown formatting inclu
    DEPRECATED="$(grep '\*\*Version\*\*:' README.md | awk -F ':' '{print $2}')"
fi

sed -i "s/$DEPRECATED/\t$VERSION/g" README.md
