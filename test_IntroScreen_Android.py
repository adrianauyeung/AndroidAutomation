__author__ = 'Adrian Au-Yeung'
# Updated Nov 16, 2015


import os
import unittest
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import sqlite3
from time import sleep

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)



class TestIntroScreen(unittest.TestCase):


    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'Android Emulator' # Android or Android Emulator
        desired_caps['app'] = '/Users/adrianwork/Automation/AndroidAutomation/ProductSingle-global-debug.apk'
        desired_caps['appPackage'] = 'com.eventbase.productsingle'
        desired_caps['appActivity'] = 'com.xomodigital.azimov.Loader'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_intro_screen_skip(self):
        # Grab navigation item from schedule DB
        conn = sqlite3.connect('productsingle.sqlite')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("select * from intro where platform = 'ios' ORDER BY sort_order ASC")
        for row in cursor:
            if row["type"] in ["plain", "login", "ibeacon"]:
                # wait for screen elements to load
                WebDriverWait(self.driver, 120).until(lambda findElem: self.driver.find_element_by_android_uiautomator( \
                    'new UiSelector().resourceId("com.eventbase.productsingle:id/title")'))

                # check title
                title = self.driver.find_element_by_android_uiautomator( \
                    'new UiSelector().resourceId("com.eventbase.productsingle:id/title")')
                self.assertEqual(title.text, row["title"])

                # check description
                desc = self.driver.find_element_by_android_uiautomator( \
                    'new UiSelector().resourceId("com.eventbase.productsingle:id/desc")')
                self.assertEqual(desc.text, row["desc"])

                # check buttons (action_text and action_skip)
                actionText = self.driver.find_element_by_android_uiautomator( \
                    'new UiSelector().resourceId("com.eventbase.productsingle:id/action_positive")')
                self.assertEqual(actionText.text, row["action_text"])

                isActionNegPresent = self.driver.find_elements_by_android_uiautomator( \
                    'new UiSelector().resourceId("com.eventbase.productsingle:id/action_negative")')

                if len(isActionNegPresent) > 0:
                    actionSkip = self.driver.find_element_by_android_uiautomator( \
                        'new UiSelector().resourceId("com.eventbase.productsingle:id/action_negative")')
                    self.assertEqual(actionSkip.text, row["action_skip"])

                # click to next screen
                if len(isActionNegPresent) > 0:
                    self.driver.find_element_by_android_uiautomator( \
                        'new UiSelector().resourceId("com.eventbase.productsingle:id/action_negative")').click()
                else:
                    self.driver.find_element_by_android_uiautomator( \
                        'new UiSelector().resourceId("com.eventbase.productsingle:id/action_positive")').click()
            else:
                pass
        cursor.close()

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestIntroScreen)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()