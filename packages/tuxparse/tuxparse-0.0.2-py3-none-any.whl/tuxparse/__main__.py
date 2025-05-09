#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import argparse
import logging
import sys
from tuxparse.boot_test_parser import BootTestParser
from tuxparse.build_parser import BuildParser
from tuxparse.test_parser import TestParser


logger = logging.getLogger()

log_parsers = {
    "boot_test": BootTestParser(),
    "build": BuildParser(),
    "test": TestParser(),
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="TuxParse, parse build, boot/test log files and print the output to the stdout."
    )

    parser.add_argument(
        "--log-file",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Log file to parser",
    )

    parser.add_argument(
        "--result-file",
        # type=argparse.FileType("rw"),
        default=None,
        help="Result JSON file to read and write too",
    )

    parser.add_argument(
        "--log-parser",
        choices=log_parsers.keys(),
        default="boot_test",
        help="Which log parser to run, when boot_test or build log-file should \
        be logs.txt or build.log, and for test it should be lava-logs.yaml",
    )

    parser.add_argument(
        "--unique",
        action="store_true",
        default=False,
        help="make unique",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Display debug messages",
    )

    args = parser.parse_args()

    if args.log_file is sys.stdin and sys.stdin.isatty():
        parser.error("Error: No input provided via stdin or --log-file. Exiting.")

    return args


def main():
    args = parse_args()
    if args.debug:
        logger.setLevel(level=logging.DEBUG)

    log_file = ""
    for line in args.log_file:
        log_file += line

    parser = log_parsers[args.log_parser]
    parser.parse_log(log_file, args.unique, args.result_file)


def start():
    if __name__ == "__main__":
        sys.exit(main())


start()
