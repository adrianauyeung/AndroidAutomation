__author__ = 'Adrian Au-Yeung'
# Updated Nov 16, 2015


import os
import unittest
import sys

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class MenuItemsCheck(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.2'
        desired_caps['deviceName'] = 'Android'
        # desired_caps['app'] = PATH('../../../Automation/AndroidAutomation/ProductSingle-global-debug.apk')
        desired_caps['appPackage'] = 'com.eventbase.productsingle'
        desired_caps['appActivity'] = 'com.xomodigital.azimov.Loader'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_screen_title(self):
        # wait for screen elements to load
        WebDriverWait(self.driver, 120).until(lambda findElem: self.driver.find_element_by_name("Open").is_displayed())

        nav = self.driver.find_element_by_name("Open")
        nav.click()

        menuitems = self.driver.find_elements_by_id("com.eventbase.productsingle:id/row_menudrawer_tab_name")
        for item in menuitems:
            if item.text != "Diagnostics":
                menuname = item.text
                item.click()
                title = self.driver.find_element_by_id("com.eventbase.productsingle:id/action_bar").\
                    find_element_by_class_name("android.widget.TextView")
                self.assertEqual(menuname, title.text)
                openmenu = self.driver.find_element_by_name("Open")
                openmenu.click()

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(MenuItemsCheck)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
