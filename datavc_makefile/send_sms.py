"""Use Africa's Talking API to send SMS to a phone number in Kenya.

This allows us to get notifications when the makefile is done running.

Usage:
    python send_sms.py <username> <phone_number> <message>

NB: You need to have the AT_API_KEY,PHONE_NUMBER,USERNAME 
environment variable set to your Africa's Talking API key.

Phone number should be in the format +2547XXXXXXXX
"""

import os
import argparse
import africastalking
import pandas as pd


# grab the API key from the environment and raise an error if it's not found
api_key = os.getenv("AT_API_KEY")
if api_key is None:
    raise ValueError("API key not found in the environment")

# Parse command line arguments
parser = argparse.ArgumentParser(description="Send SMS using Africa's Talking API")
parser.add_argument("username", help="Your Africa's Talking username")
parser.add_argument("recipients", nargs="+", help="Phone number(s) of the recipient(s)")
parser.add_argument("message", help="Message to send")
args = parser.parse_args()

# Initialize the SDK
africastalking.initialize(args.username, api_key)

# Get the SMS service
SMS = africastalking.SMS

# Send the message
try:
    response = SMS.send(args.message, args.recipients)
    print(response)

    # get the status, status_code, and message
    # store the result in a pandas dataframe and write to a csv file
    # for easy monitoring
    results = []
    # to handle multiple recipients
    for recipient in args.recipients:
        result = {
            "status": response["SMSMessageData"]["Recipients"][0]["status"],
            "status_code": response["SMSMessageData"]["Recipients"][0]["statusCode"],
            "recipient": recipient,
            "message_id": response["SMSMessageData"]["Recipients"][0]["messageId"],
            "cost": response["SMSMessageData"]["Recipients"][0]["cost"],
        }

        # add datatypes to the result
        result["status"] = str(result["status"])
        result["status_code"] = str(result["status_code"])
        result["message_id"] = str(result["message_id"])
        result["cost"] = str(result["cost"])

        results.append(result)

    # store the results in a pandas dataframe and write to a parquet file
    df = pd.DataFrame(results)
    df.to_parquet("output/sms_result.parquet")
except Exception as e:
    print(f"An error occurred: {str(e)}")
