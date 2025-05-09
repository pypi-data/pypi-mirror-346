#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import io
import json
import logging
import re
import yaml
from yaml import SafeLoader
from collections import defaultdict
from tuxparse.lib.base_log_parser import (
    BaseLogParser,
    REGEX_NAME,
    REGEX_EXTRACT_NAME,
    tstamp,
    pid,
    not_newline_or_plus,
)

logger = logging.getLogger()

MULTILINERS = [
    (
        "exception",
        rf"-+\[? cut here \]?-+.*?{tstamp}{pid}?\s+-+\[? end trace \w* \]?-+",
        rf"\n{tstamp}{not_newline_or_plus}*",
    ),  # noqa
    (
        "kasan",
        rf"{tstamp}{pid}?\s+=+\n{tstamp}{pid}?\s+BUG: KASAN:.*?\n*?{tstamp}{pid}?\s+=+",
        rf"BUG: KASAN:{not_newline_or_plus}*",
    ),  # noqa
    (
        "kcsan",
        rf"{tstamp}{pid}?\s+=+\n{tstamp}{pid}?\s+BUG: KCSAN:.*?=+",
        rf"BUG: KCSAN:{not_newline_or_plus}*",
    ),  # noqa
    (
        "kfence",
        rf"{tstamp}{pid}?\s+=+\n{tstamp}{pid}?\s+BUG: KFENCE:.*?{tstamp}{pid}?\s+=+",
        rf"BUG: KFENCE:{not_newline_or_plus}*",
    ),  # noqa
    (
        "panic-multiline",
        rf"{tstamp}{pid}?\s+Kernel panic - [^\n]+\n.*?-+\[? end Kernel panic - [^\n]+ \]?-*",
        rf"Kernel {not_newline_or_plus}*",
    ),  # noqa
    (
        "internal-error-oops",
        rf"{tstamp}{pid}?\s+Internal error: Oops.*?-+\[? end trace \w+ \]?-+",
        rf"Oops{not_newline_or_plus}*",
    ),  # noqa
]

ONELINERS = [
    ("oops", r"^[^\n]+Oops(?: -|:).*?$", rf"Oops{not_newline_or_plus}*"),  # noqa
    (
        "fault",
        r"^[^\n]+Unhandled fault.*?$",
        rf"Unhandled {not_newline_or_plus}*",
    ),  # noqa
    ("warning", r"^[^\n]+WARNING:.*?$", rf"WARNING:{not_newline_or_plus}*"),  # noqa
    (
        "bug",
        r"^[^\n]+(?: kernel BUG at|BUG:).*?$",
        rf"BUG{not_newline_or_plus}*",
    ),  # noqa
    (
        "invalid-opcode",
        r"^[^\n]+invalid opcode:.*?$",
        rf"invalid opcode:{not_newline_or_plus}*",
    ),  # noqa
    (
        "panic",
        r"Kernel panic - not syncing.*?$",
        rf"Kernel {not_newline_or_plus}*",
    ),  # noqa
]

# Tip: broader regexes should come first
REGEXES = MULTILINERS + ONELINERS


class BootTestParser(BaseLogParser):
    def __cutoff_boot_log(self, log):
        split_patterns = [r" login:", r"console:/", r"root@(.*):[/~]#"]
        split_index = None

        for pattern in split_patterns:
            match = re.search(pattern, log)
            if match:
                # Find the earliest split point
                if split_index is None or match.start() < split_index:
                    split_index = match.start()

        if split_index is not None:
            boot_log = log[:split_index]
            test_log = log[split_index:]
            return boot_log, test_log

        # No match found; return whole log as boot log
        return log, ""

    def __kernel_msgs_only(self, log):
        kernel_msgs = re.findall(f"({tstamp}{pid}? .*?)$", log, re.S | re.M)  # noqa
        return "\n".join(kernel_msgs)

    def logs_txt(self, f_in):

        f_text = io.StringIO()

        for line in io.StringIO(f_in):
            line = line.rstrip("\n")
            try:
                data = yaml.load(line, Loader=SafeLoader)
                data = data[0]
            except TypeError:
                print(line)
                continue
            except yaml.YAMLError:
                print(line)
                continue
            if not data or not isinstance(data, dict):
                print(line)
                continue
            if not set(["dt", "lvl", "msg"]).issubset(data.keys()):
                print(line)
                continue

            if data["lvl"] not in ["target", "feedback"]:
                continue

            if data["lvl"] == "feedback" and "ns" in data:
                f_text.write(f"<{data['ns']}> ")
            f_text.write(data["msg"] + "\n")
        return f_text.getvalue()

    def parse_log(self, log_file, unique, result_file):
        # If running as a SQUAD plugin, only run the boot/test log parser if this is not a build testrun
        if log_file is None:
            return

        first_line = log_file.strip().splitlines()[0]
        if first_line.startswith('- {') and first_line.endswith('}'):
            log_file = self.logs_txt(log_file)
            with open("logs.txt", "w", encoding="utf-8") as f_txt:
                f_txt.write(log_file)

        boot_log, test_log = self.__cutoff_boot_log(log_file)
        logs = {
            "boot": boot_log,
            "test": test_log,
        }

        results = defaultdict(
            lambda: defaultdict(lambda: {"log_lines": "", "result": "fail"})
        )
        for log_type, log in logs.items():
            log = self.__kernel_msgs_only(log)
            suite_name = f"log-parser-{log_type}"

            regex = self.compile_regexes(REGEXES)
            matches = regex.findall(log)
            snippets = self.join_matches(matches, REGEXES)

            for regex_id in range(len(REGEXES)):
                test_name = REGEXES[regex_id][REGEX_NAME]
                regex_pattern = REGEXES[regex_id][REGEX_EXTRACT_NAME]
                test_name_regex = None
                if regex_pattern:
                    test_name_regex = re.compile(regex_pattern, re.S | re.M)
                tests_without_shas_to_create, tests_with_shas_to_create = (
                    self.create_tests(
                        suite_name, test_name, snippets[regex_id], test_name_regex
                    )
                )
                if not unique:
                    for name, lines in tests_without_shas_to_create.items():
                        results[suite_name][name]["log_lines"] = list(lines)
                for name, lines in tests_with_shas_to_create.items():
                    results[suite_name][name]["log_lines"] = list(lines)

        if result_file:
            with open(result_file, "r") as json_file:
                data = json.load(json_file)
        else:
            data = defaultdict(lambda: {})

        data.update(results)
        if result_file:
            with open(result_file, "w") as json_file:
                json.dump(data, json_file, indent=4)
        else:
            print(json.dumps(data, indent=4))
