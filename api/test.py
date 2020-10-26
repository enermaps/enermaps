"""Simplified entrypoint for discovering and running all test of the project
"""
import unittest

import app

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover("app/")
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)
