import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os

class SeleniumCBT(unittest.TestCase):
    def setUp(self):
        self.username = os.environ['CBT_USERNAME']
        self.authkey  = os.environ['CBT_APIKEY']
       
        self.api_session = requests.Session()
        self.api_session.auth = (self.username,self.authkey)
        self.test_result = None

        caps = {}
        caps['name'] = os.environ['CBT_BUILD_NAME']
        caps['build'] = os.environ['CBT_BUILD_NUMBER']
        caps['browser_api_name'] = os.environ['CBT_BROWSER']
        caps['os_api_name'] = os.environ['CBT_OPERATING_SYSTEM']
        caps['screen_resolution'] = os.environ['CBT_RESOLUTION']
        caps['record_video'] = 'true'    

        try:
            self.driver = webdriver.Remote(
            desired_capabilities=caps, 
            
            command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(self.username, self.authkey))
          
        except Exception as e:
            raise e
        
    def test_homepage(self):
        try:
            self.driver.implicitly_wait(10)
            
            self.driver.get('https://google.com')     
            
            self.assertEqual(self.driver.title, 'Google')

            self.test_result = 'pass'
            
        except AssertionError as e:
            # log the error message, and set the score
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots/' + snapshot_hash,
                data={'description':"AssertionError: " + str(e)})
            self.test_result = 'fail'
            
     
        self.driver.quit()
        # Here we make the api call to set the test's score
        # Pass if it passes, fail if an assertion fails, unset if the test didn't finish
        if self.test_result is not None:
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id,
                data={'action':'set_score', 'score':self.test_result})
            
        if self.test_result is 'pass':
            pass
        else:
            fail
            
    def test_login(self):
        try:
            self.driver.implicitly_wait(10)
            
            self.driver.get('https://smartbear.com')     
            
            self.assertEqual(self.driver.title, 'Google')

            self.test_result = 'pass'
            
        except AssertionError as e:
            # log the error message, and set the score
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots/' + snapshot_hash,
                data={'description':"AssertionError: " + str(e)})
            self.test_result = 'fail'
                 
        self.driver.quit()
        # Here we make the api call to set the test's score
        # Pass if it passes, fail if an assertion fails, unset if the test didn't finish
        if self.test_result is not None:
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id,
                data={'action':'set_score', 'score':self.test_result})
            
        if self.test_result is 'pass':
            pass
        else:
            fail
                
if __name__ == '__main__':
    unittest.main()
