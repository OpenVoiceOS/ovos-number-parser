"""Strict xfails for the test rows that numtag reads differently from the old
readers.

``numtag_xfail.json`` maps a test id to its rows, and each row to the URL of
the issue that tracks it. The key ``""`` stands for the assertions of the test
outside its subtests. A subtest key is the subtest parameters as ``repr``
writes them (``lang='fr', text='à tout le moins 3 jours'``), after the subtest
message in brackets when it has one.

A listed test or subtest that passes fails the run, so a fixed issue shows up
as soon as numtag ships the fix and its rows can leave the file. An exception
other than an ``AssertionError`` is no expected failure and fails the run.
"""
import json
import unittest
from contextlib import contextmanager
from pathlib import Path

import pytest

XFAILS = json.loads((Path(__file__).parent / "numtag_xfail.json").read_text(encoding="utf-8"))

#: the subtest rows of the running test
_running = {}


def subtest_key(subtest) -> str:
    """``[message] key=value, ...`` of a unittest subtest."""
    params = ", ".join(f"{key}={value!r}" for key, value in subtest.params.items())
    if subtest._message is unittest.case._subtest_msg_sentinel:
        return params
    return f"[{subtest._message}] {params}"


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item):
    _running["rows"] = XFAILS.get(item.nodeid, {})
    try:
        return (yield)
    finally:
        del _running["rows"]


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    rows = XFAILS.get(item.nodeid, {})
    # a subtest reports while its test runs; the test body reports after it
    if call.when != "call" or "" not in rows or "rows" in _running:
        return report
    if report.failed and call.excinfo is not None and call.excinfo.errisinstance(AssertionError):
        report.outcome, report.wasxfail = "skipped", rows[""]
    elif report.passed:
        report.outcome, report.longrepr = "failed", f"[XPASS(strict)] {rows['']}"
    return report


_subTest = unittest.TestCase.subTest


@contextmanager
def _subtest(self, msg=unittest.case._subtest_msg_sentinel, **params):
    with _subTest(self, msg, **params):
        url = _running.get("rows", {}).get(subtest_key(self._subtest))
        if not url:
            yield
            return
        try:
            yield
        except AssertionError:
            pytest.xfail(url)
        pytest.fail(f"[XPASS(strict)] {url}", pytrace=False)


unittest.TestCase.subTest = _subtest
