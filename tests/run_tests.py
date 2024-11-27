#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import tests.test_trains as task_1

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suites = unittest.TestSuite()

    suites.addTests(loader.loadTestsFromModule(task_1))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suites)
