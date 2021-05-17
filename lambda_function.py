import json
import os
import requests
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

def lambda_handler(event, context):
    url = os.environ["api_url"]
    recipient = os.environ["recipient"]
    region = os.environ['AWS_REGION']
    telegram_api_url = os.environ["telegram_api_url"]
    channel_id = os.environ["channel_id"]
    client = boto3.client('ses',region_name=region)
    details = get_availablity_details(url)
   
    print(details)
    if len(details) > 0:
        send_email_util(client, recipient, details)
        send_telegram_bot_notification(telegram_api_url, channel_id, details)

def get_availablity_details(url):
    details = ""
    params = {'district_id': 571, 'date': datetime.today().strftime('%d-%m-%Y')}
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url = url, headers = headers, params = params)
    if(response.status_code == 200):
        response_json = response.json()
        for center in response_json["centers"]:
            for session in center["sessions"]:
                if (session["min_age_limit"] == 18 and session["available_capacity"] > 0):
                    details += "Center Name: " +center["name"] + "\nPincode: "+str(center["pincode"])+"\nAvailable Date: " + session["date"] + "\nCapacity: "+ str(session["available_capacity"]) + "\n\n"
    return details

def send_email_util(client, recipient, details):
    charset = "UTF-8"
    sender = recipient
    body = details
    subject = "Vaccination Availability"
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
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

def send_telegram_bot_notification(telegram_api_url, channel_id, details):
    params = {'chat_id': channel_id, 'text': details}
    requests.post(url = telegram_api_url, params = params)
