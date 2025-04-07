import os
import time
import requests
import base64
import json
import logging

from clueCreate import clueCreate

logging.basicConfig(
    level=logging.INFO,  # Set minimum log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named "app.log"
        logging.StreamHandler()  # Also output logs to the console
    ]
)



# WEBSITE_LINK = os.getenv("WEBSITE_LINK")
# api_base_url = "http://localhost:3000/api/v4" 
# api_base_url = "http://host.docker.internal:3000/api/v4"
# api_base_url = "http://192.168.6.59:12345/api/v4/" # (zf 9)
# api_base_url = "http://192.168.137.225:3000/api/v4/" # (zf 8)

WEBSITE_LINK = os.getenv("WEBSITE_LINK", "http://host.docker.internal:3000/api/v4" )
api_base_url = WEBSITE_LINK

username = "api_client"
password = "hellohello"
encoded_credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
headers = {
    "accept": "application/json",
    "Authorization": f"Basic {encoded_credentials}"
}

cid = os.getenv("CID", "1")
# cid = "1"
processed_submissions = set()

def pollJudgements():
    url = f"{api_base_url}/contests/{cid}/judgements"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info("Successfully polled judgements.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error polling judgements: {e}")
        return None

def readSubmission(submissionID):
    def my_func_1():
        url = f"{api_base_url}/contests/{cid}/submissions/{submissionID}/source-code"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            try:
                content = base64.b64decode(data[0]['source']).decode('utf-8')
            except UnicodeDecodeError as ude:
                logging.error(f"Unicode decode error for submission ID {submissionID}: {ude}")
                return None
            logging.info(f"Successfully retrieved source code for submission ID: {submissionID}")
            return content
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving source code for submission ID: {submissionID} - {e}")
            return None

    url = f"{api_base_url}/contests/{cid}/submissions/{submissionID}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        teamID = data["team_id"]
        problemID = data["problem_id"]
        logging.info(f"Successfully retrieved submission details for submission ID: {submissionID}")
        return my_func_1(), teamID, problemID
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving submission details for submission ID: {submissionID} - {e}")
        return None, None, None
        
def postClar(clue, team_id, problemID):
    data = {
        'text': clue,
        'problem_id': problemID,
        'to_team_id': team_id
    }

    url = f"{api_base_url}/contests/{cid}/clarifications"
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status() 
        response_data = response.json() 
        logging.info(f"Successfully posted clarification: {json.dumps(response_data, indent=4)}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error posting clarification: {e}")
        if e.response:
            logging.error(f"Response content: {e.response.text}")

from datetime import datetime, timezone, timedelta

now = datetime.now()
local_tz = timezone(timedelta(hours=5, minutes=30)) 
now = now.astimezone(local_tz)

def main_workflow():
    while True:
        judgements = pollJudgements()
        
        if judgements:
            for judgement in judgements:
                submission_id = judgement['submission_id']
                judgement_start_time = judgement['start_time']
                
                if not isinstance(judgement_start_time, str):
                    logging.error(f"Expected string for judgement['start_time'], but got {type(judgement_start_time)}")
                    continue
                
                judgement_start_time = datetime.fromisoformat(judgement_start_time)
                
                # Skip if the submission has already been processed or is "AC" or the judgement start time is in the past
                if (submission_id in processed_submissions) or (judgement['judgement_type_id'] == "AC") or (judgement_start_time < now):
                    continue

                processed_submissions.add(submission_id)  # Mark this submission as processed
                logging.info(f"Processing submission id: {submission_id}")

                source_code, team_id, problemID = readSubmission(submission_id)
                if source_code is None or team_id is None or problemID is None:
                    logging.error(f"Failed to process submission ID: {submission_id} due to previous errors.")
                    continue

                logging.info(f"The source code is \n {source_code} \n\n The Team id is {team_id} \n\n The Problem id is {problemID}")
                
                clue = clueCreate(source_code, problemID)
                logging.info("The created clue is as follows:- ")
                logging.info(clue)
                postClar(clue, team_id, problemID)
                logging.info("-" * 122)
                
        # Poll every 10 seconds, can be adjusted
        time.sleep(10)

main_workflow()