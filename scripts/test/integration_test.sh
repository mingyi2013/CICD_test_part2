#!/usr/bin/env bash

# Copyright (C) 2022 Roberto Rossini (roberros@uio.no)
# SPDX-License-Identifier: MIT

set -u
set -e
set -o pipefail

# This script automates the following steps:
# - Encrypt the file passed as second argument using the key passed as third argument
# - Decrypt the encrypted file using the same key
# - Check that the original file and the decrypted file are identical

# Make sure the script is being called with the correct number of arguments
ARGC=$#
if [ $ARGC -ne 3 ]; then
    2>&1 echo "Usage:   $0 path_to_cryptonite test_file key"
    2>&1 echo "Example: $0 venv/bin/cryptonite test_file.txt 13"
    exit 1
fi


cryptonite="$1"
CRYPTONITE_KEY="$3"
export CRYPTONITE_KEY

# If plain_file is a pipe, first copy the file to a temporary file
if [ -p "$2" ]; then
    plain_file="$(mktemp)"
    trap 'rm -f "$plain_file"' EXIT

    cat "$2" >> "$plain_file"
else
    plain_file="$2"
fi

# Run cryptonite encrypt | cryptonite decrypt, then compare with the input file and report differences (if any)
function test_cryptonite_roundtrip {
    set -u
    set -e
    set -o pipefail

    file="$1"

    diff --brief \
         --report-identical-files \
         "$file" \
         <("$cryptonite" encrypt --no-validate-input < "$file" | "$cryptonite" decrypt --no-validate-input)
}


# Run test and exit with code 1 in case one or more differences are found
if test_cryptonite_roundtrip "$plain_file"; then
    2>&1 echo '### PASS! ###'
else
    2>&1 echo '### FAIL! ###'
    exit 1
fi
