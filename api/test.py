#!/usr/bin/env python3
"""Simplified entrypoint for discovering and running all test of the project
"""
import argparse
import sys
import unittest

import app  # NOQA
from app.common.test import LabelTestRunner


def get_parser():
    """Return the argument parser for the test runner"""
    parser = argparse.ArgumentParser(__name__)
    parser.add_argument(metavar="label", action="append", nargs="*", dest="labels")
    return parser


if __name__ == "__main__":
    arg_parser = get_parser()
    args = arg_parser.parse_args()
    loader = unittest.TestLoader()
    tests = loader.discover("app/")
    testRunner = LabelTestRunner(args.labels)
    result = testRunner.run(tests)
    if not result.wasSuccessful():
        sys.exit(1)
