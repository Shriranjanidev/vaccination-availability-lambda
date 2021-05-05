import json
import os
import requests
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

def lambda_handler(event, context):
    url = os.environ["api_url"]
    recepient = os.environ["recepient"]
    region = os.environ['AWS_REGION']
    
    client = boto3.client('ses',region_name=region)
    start_date = datetime.today()
    end_date = datetime.today() + timedelta(days=30)

    availability_list = get_availablity_details(url, start_date, end_date)
   
    print(json.dumps(availability_list))
    if availability_list:
        send_email_util(client, recepient, availability_list)

def get_availablity_details(url, start_date, end_date):
    availability_list = []
    while start_date <= end_date:
        params = {'district_id': 571, 'date': datetime.today().strftime('%d-%m-%Y')}
        response = requests.get(url = url, params = params)
        if(response.status_code == 200):
            response_json = response.json()
            for center in response_json["centers"]:
                for session in center["sessions"]:
                    if (session["min_age_limit"] == 18 and session["available_capacity"] > 0):
                        availability = {
                            "centerName": center["name"],
                            "availableDate": session["date"],
                            "availableCapacity": session["available_capacity"],
                            "slots": session["slots"]
                        }              
                        availability_list.append(availability)
        start_date = start_date + timedelta(days=7)
    return availability_list

def send_email_util(client, recepient, availability_list):
    charset = "UTF-8"
    sender = recepient
    body = json.dumps(availability_list)
    subject = "Vaccination Availability"
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recepient,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': charset,
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    
