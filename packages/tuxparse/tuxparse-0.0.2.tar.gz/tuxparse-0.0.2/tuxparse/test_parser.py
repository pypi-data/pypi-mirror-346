#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import json
import logging
import re
import sys
import yaml
from collections import defaultdict
from tuxparse.lib.base_log_parser import (
    BaseLogParser,
)

logger = logging.getLogger()


class LineNumberLoader(yaml.SafeLoader):

    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep)
        mapping["_line_number"] = node.start_mark.line + 1
        return mapping


class TestParser(BaseLogParser):

    def process_test_suites(self, test_suite, log_lines):
        for test_name, test_data in test_suite.items():
            if isinstance(test_data, dict):
                starttc = test_data.get("starttc")
                endtc = test_data.get("endtc")

                if isinstance(starttc, int) and isinstance(endtc, int):
                    test_data["log_lines"] = [
                        f"{message}"
                        for line, message, line_number in log_lines
                        if starttc <= line_number <= endtc
                    ]

                self.process_test_suites(test_data, log_lines)

    def parse_log(self, log_file, unique, result_file):

        if not result_file:
            logger.error("need a result file")
            sys.exit(1)
        log_data = yaml.load(log_file, Loader=LineNumberLoader)
        log_lines = []
        for entry in log_data:
            if isinstance(entry, dict) and "dt" in entry and "msg" in entry:
                try:
                    line = entry["dt"]
                    message = entry["msg"]
                    line_number = entry.get("_line_number", None)
                    log_lines.append((line, message, line_number))
                except ValueError:
                    print(f"Skipping log entry with invalid line: {entry['dt']}")

        with open(result_file, "r") as json_file:
            data = json.load(json_file)

        self.process_test_suites(data, log_lines)

        with open(result_file, "w") as json_file:
            json.dump(data, json_file, indent=4)
