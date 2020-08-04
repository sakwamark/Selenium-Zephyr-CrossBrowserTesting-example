# Selenium-Zephyr-CrossBrowserTesting-example
In this repository, we will highlight an example of integrating test management, cross browser testing with Selenium, Jira, and Jenkins CI. 

Test Management and Cross Browser Testing are done using two world-class SmartBear solutions; Zephyr for Jira and CrossBrowserTesting.

### CrossBrowserTesting
Ditch your VMs and Device Lab. Easily run Manual, Visual, and Selenium Tests in the cloud on 2050+ real desktop and mobile browsers.
https://crossbrowsertesting.com/

### Zephyr for Jira
The #1 Agile Test Management Solution in Jira, perfect for teams focusing on Test Design, Execution, and Test Automation
https://marketplace.atlassian.com/apps/1014681/zephyr-for-jira-test-management?hosting=cloud&tab=overview

### Workflow
With these solutions, we can seamlessly execute a Jenkins CI job with a selenium test executing on a real machine from CrossBrowserTesting and results automatically synchronized into Jira via a Zephyr test cycle. This workflow requires being an active user on both tools. 

1. Install the CrossBrowserTesting Jenkins plugin 
https://help.crossbrowsertesting.com/selenium-testing/continuous-integration/installing-jenkins/

1. Download Selenium Tests (selenium_test.py) and Zephyr for Jira Synchronize Script (sync_z4j.py) example from this repo

1. Fill out parameters in config.json file to be authenticated into Zephyr for Jira https://zephyrdocs.atlassian.net/wiki/spaces/ZFJCLOUD/pages/1686798372/A.T.O.M+API+Documentation

1. Set up Jenkins Job with both tools
  1. Enable CrossBrowserTesting.com in Build Environment according to above docs. Select desired OS, Browser, and Resolution
  https://help.crossbrowsertesting.com/wp-content/uploads/2019/06/Build_Environment_1.png
  
  1. Set up first build step to run selenium tests and execute junit xml file as the report
      1. Note: This can be done in many ways. During the webinar, I used the shining panda jenkins plugin with the pytest module to do this. 
      Sample Command - py.test --junitxml "/Results/results.xml" "selenium_test.py"
  
  1. Set up execution for Z4J Sync scriptas a build or post-build action
      1. Sample Command - python sync_z4j.py
      
Screenshots from my demo:
https://gyazo.com/c77b1ca8c713509f43ba65ca267b9c6e
https://gyazo.com/900c0e33d4180c3d154096287b7bf516

## Sync Z4J Script

This Script uses three api calls to do the following:
  1. Generate JWT Token
  1. Create Zephyr Test Automation Job: Indicating automation type, where results are located, and which test cycle to sync them too
  1. Execute Job with create job id
  
  You can add more API calls to update and delete jobs as well. https://zephyrdocs.atlassian.net/wiki/spaces/ZFJCLOUD/pages/1686798372/A.T.O.M+API+Documentation

You can see this in action during our SmartBear Webinar - Test, Track, and Analyze: Scaling Test Automation Effectively in Agile
https://smartbear.com/resources/webinars/scaling-test-automation-in-agile/



## Configuration Instructions
config.json file is required in the same directory as the migration script. 

Example config can be found 

ACCESS_KEY: Output Directory for Reports.

SECRET_KEY: Vendor ID issued by Atlassian.

ACCOUNT_ID: ID of Vendor Add-on

PROJECT_ID: Email of account with Reporting Permissions to Vendor Account.

REPORT_DIRECTORY: Password of account with Reporting Permissions to Vendor Account.

RESULT_FILE: Array(List) of files that contain search text *NOTE Files should be single column csv with search terms.

All fields are required. 

