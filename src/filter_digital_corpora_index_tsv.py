#!/usr/bin/env python3

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

import argparse
import csv
import logging
import urllib.parse
from typing import Set


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("in_tsv", type=argparse.FileType("r"))
    parser.add_argument("subjects_txt", type=argparse.FileType("r"))
    parser.add_argument("out_tsv", type=argparse.FileType("x"))
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    reader = csv.DictReader(args.in_tsv, delimiter="\t")

    # Assert type for static type review.
    assert isinstance(reader.fieldnames, list)

    writer = csv.DictWriter(args.out_tsv, delimiter="\t", fieldnames=reader.fieldnames)

    s3keys: Set[str] = set()
    for line in args.subjects_txt:
        cleaned_line = line.strip()
        s3key = urllib.parse.unquote(
            cleaned_line.replace("https://digitalcorpora.s3.amazonaws.com/", "")
        )
        s3keys.add(s3key)

    writer.writeheader()

    # Filter the incoming rows according to subjects_txt.
    for row in reader:
        s3key = row["s3key"]
        if s3key not in s3keys:
            continue
        s3keys.remove(s3key)
        writer.writerow(row)

    if len(s3keys) > 0:
        for s3key in sorted(s3keys):
            logging.error(s3key)
        raise ValueError("Some subjects were not found in the Digital Corpora index.")


if __name__ == "__main__":
    main()
