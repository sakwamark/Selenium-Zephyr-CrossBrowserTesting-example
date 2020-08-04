import json
import os
import requests
from pathlib import Path

with open('config.json', 'r') as file:
    config = json.load(file)

#Load all parameters from config.json for authentication, results, and jira project
access_key = config['ACCESS_KEY']
secret_key = config['SECRET_KEY']
account_id = config['ACCOUNT_ID']

project_id = config['PROJECT_ID']
report_directory = config['REPORT_DIRECTORY']
result_file = config['RESULT_FILE']

#-----------------------------------------------------------------------------------------------------------------------
#Generate JWT Token for authentication
generate_jwt_url = 'https://prod-vortexapi.zephyr4jiracloud.com/api/v1/jwt/generate'
payload = {'accessKey': access_key,'secretKey': secret_key,'accountId': account_id}
headers = {'Content-Type': 'application/json'}
jwt_token_request = requests.post(generate_jwt_url, data=json.dumps(payload), headers=headers)

jwt_token=jwt_token_request.text

if jwt_token_request.status_code == 200 and 'JWT' in jwt_token_request.text :
    print('JWT Token Generated Successfully')
else:
    print('Error Generating JWT Token:' + str(jwt_token_request.status_code) + ' - ' + jwt_token_request.text)
#----------------------------------------------------------------------------------------------------------------------
#Create Selenium Job in Z4J
create_job_url = 'https://prod-vortexapi.zephyr4jiracloud.com/api/v1/automation/job/create'
headers= {'accessKey': access_key, 'jwt': jwt_token}

data_folder = Path(report_directory)

print('Using Results File in ' + str(data_folder/'results.xml'))

payload = {'jobName': 'CBT Selenium Test',
'automationFramework': 'SELENIUM',
'cycleName': 'JenkinsTests',
'folderName': 'Jenkins',
'versionName': 'Unscheduled',
'projectKey': project_id, #Numeric Project Key for Jira Project
'createNewCycle': 'true',
'createNewFolder': 'true',
'jobDescription': 'Test Executed from Selenium through CBT'
}

files = [
  ('file', open(data_folder/result_file,'rb'))
]

create_job_request = requests.request("POST", create_job_url, headers=headers, data=payload, files=files )
request_text = create_job_request.text

if create_job_request.status_code == 200 and 'Job has been successfully created' in create_job_request.text:
    print('Successfully Created Z4J Job')
else:
    print('Error creating Z4J Job: ' + str(create_job_request.status_code) + ' - ' + create_job_request.text)
          
#----------------------------------------------------------------------------------------------------------------------
# Get Job Id from response
# Response Format { "message": "Job has been successfully created, Job id is : 726FAE2BD1280BCED437FE7582885F7CB1FE97C1A8D10ADEF6F1B1D239A51642"}
job_id = request_text[request_text.index(' : ')+3:].replace('"}','')

print('Job ID Created - ' + job_id)

#Execute Z4J Job to Sync Selenium Results 
execute_job_url = "https://prod-vortexapi.zephyr4jiracloud.com/api/v1/automation/job/execute"

payload = {'jobId': job_id}

execute_job_request = requests.post(execute_job_url, headers=headers, data=payload)

if execute_job_request.status_code == 200 and 'Job executed successfully' in execute_job_request.text:
    print('Zephyr for Jira Job Executed')
else:
    print('Error executing job: ' + str(execute_job_request.status_code) + ' - ' + execute_job_request.text)
