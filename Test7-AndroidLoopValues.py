from appium import webdriver
from time import sleep
import serial
import sys
import os
import unittest
import datetime
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

''' CONFIGURATION'''
DEVICE = '19b801a117'  #19b801a117  #0a5c01c342e18297
DEVICENAME= 'Android'
APPIUM_URL = 'http://localhost:4723/wd/hub'
DRIVER = None
'''
This Function Sends Appium Commands and listens to the Serial port.
'''

class AndroidDateTests(unittest.TestCase):
	"Class to run tests against the Lotus APP"
	def setUp(self):		
		print "\nSetup\n"
		desired_caps1 = {}
		desired_caps1['platformName'] = DEVICENAME
		desired_caps1['platformVersion'] = '4.2'
		desired_caps1['deviceName'] = DEVICE
		desired_caps1['device'] = DEVICENAME 		
		desired_caps1['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__),'app/LotusApp-debug.apk'))
		desired_caps1['appPackage'] = 'com.ge.med.mic.lotus'
		desired_caps1['appActivity'] = 'com.ge.med.mic.lotus.activities.LotusMonitoringActivity'
		desired_caps1['useKeyStore']= 0		
		#self.driver = webdriver.Remote(APPIUM_URL, desired_caps1)
		self.driver = webdriver.Remote(APPIUM_URL, desired_caps1)
		         
	def test_getDate(self):		
		for i in range(1,100):
			sys_date = self.driver.find_element_by_id('com.ge.med.mic.lotus:id/us1_fhr')
			elem_date = sys_date.text
			print elem_date
			print datetime.datetime.now()
		
	def tearDown(self):
		"Tear down the test"
		#self.driver.quit()


#---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidDateTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
    print "End\n"
