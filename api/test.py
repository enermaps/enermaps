import unittest

import app

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover("app/")
    print(tests)
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)

    # unittest.main()
