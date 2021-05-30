# Vaccination Availability

This repository contains lambda code to send email notification to recipient email address and a telegram channel through Telegram Bots, if slots are available in vaccination centre in Chennai district

**Pre-requisite Steps**
- Create a lambda function with Python runtime.
- Configure scheduler event using AWS Event Bridge for every 1 minute(This can be configured as per your convenience) with the lambda as target
- Configure AWS SES by verifying the sender email

**Lambda Configuration Steps:**
- Create the following environment variables:
    - api_url: Get the URL from cowin website (Open API tab)
    - recipient: <email_address>
    - telegram_api_url: Telegram Bot API URL with bot token
    - chat_id: Telegram channel id
- Attach AWS SES policy to lambda execution role
- Download the code in repository and upload the zip of the project in AWS Lambda
- Deploy the code changes in AWS lambda

**Important Information:**
- Scheduler, AWS Lambda and AWS region should be configured in the same AWS region

**Diagram:**

<img src="./vaccination_availability_notification_arch.png" width="900"/>
