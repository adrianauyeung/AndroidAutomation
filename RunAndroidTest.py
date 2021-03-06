__author__ = 'Adrian Au-Yeung'
# Updated Nov 16, 2015

import os
import unittest
import datetime

now = datetime.datetime.now()
def result():
        scriptPath = os.path.dirname(__file__)
        file = os.path.join(scriptPath, log_file)
        if 'FAILED' in open(file).read():
            os.rename(file, file.replace("inProgress", "FAILED"))
        else:
            os.rename(file, file.replace("inProgress", "PASSED"))


class AndroidTests():
    def suite(self): # Function stores all the modules to be tested
        modules_to_test = []
        test_dir = os.listdir('.')
        for test in test_dir:
            if test.startswith('test') and test.endswith('Android.py'):
                modules_to_test.append(test.rstrip('.py'))

        alltests = unittest.TestSuite()
        for module in map(__import__, modules_to_test):
            module.testvars = ["variables you want to pass through"]
            alltests.addTest(unittest.findTestCases(module))
        return alltests



if __name__ == '__main__':
    androidTests = AndroidTests()
    unittest.main(defaultTest='androidTests.suite', verbosity=2)


