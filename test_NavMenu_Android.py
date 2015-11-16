#!/usr/local/Cellar/python3/3.5.0/Frameworks/Python.framework/Versions/3.5/bin/python3.5
__author__ = 'adrian au-yeung'


import os
import unittest
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request
import sqlite3
import sys

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# Download the Product Single database
# urllib.request.urlretrieve("https://staging-webservice.eventbase.com/v1/admin/product/database/legacy-info/?method=\
# db_content&cid=productsingle&pid=productsingle","productsingle.sqlite")


class TestMenuItemsCheck(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.2'
        desired_caps['deviceName'] = 'Android'
        # desired_caps['app'] = PATH('../../../Automation/AndroidAutomation/ProductSingle-global-debug.apk')
        desired_caps['appPackage'] = 'com.eventbase.productsingle'
        desired_caps['appActivity'] = 'com.xomodigital.azimov.Loader'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_menu_items(self):
        # Grab navigation item from schedule DB
        con = sqlite3.connect("productsingle.sqlite")
        cur = con.cursor()
        dbMenu = [row[0] for row in cur.execute("select title from navigation where device = 'iPhone' ORDER BY \
        sort_order ASC")]

        # wait for screen elements to load
        WebDriverWait(self.driver, 120).until(lambda findElem: self.driver.find_element_by_name("Open").is_displayed())

        # Open navigation menu
        nav = self.driver.find_element_by_name("Open")
        nav.click()

        # Compare if db menu = app menu
        appMenu = []
        for item in self.driver.find_elements_by_id("com.eventbase.productsingle:id/row_menudrawer_tab_name"):
            appMenu.append(item.text)
        self.assertEqual(appMenu, dbMenu)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestMenuItemsCheck)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()