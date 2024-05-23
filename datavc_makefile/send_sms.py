"""Use Africa's Talking API to send SMS to a phone number in Kenya.

This allows us to get notifications when the makefile is done running.

Usage:
    python send_sms.py <phone_number> <message>
"""

import os
import argparse
import africastalking
import pandas as pd


# Initialize SDK
username ="jak2"
api_key = os.getenv("AT_API_KEY")
africastalking.initialize(username, api_key)

# Get the SMS service
sms = africastalking.SMS

# Parse command line arguments
parser = argparse.ArgumentParser(description="Send SMS using Africa's Talking API")
parser.add_argument("recipients", nargs="+", help="Phone number(s) of the recipient(s)")
parser.add_argument("message", help="Message to send")
args = parser.parse_args()

# Send the message
try:
    response = sms.send(args.message, args.recipients)
    print(response)
    # get the status, status_code, and message
    # store the result in a pandas dataframe and write to a csv file
    # for easy monitoring
    result = {
        "status": response["SMSMessageData"]["Recipients"][0]["status"],
        "status_code": response["SMSMessageData"]["Recipients"][0]["statusCode"],
        "message": response["SMSMessageData"]["Recipients"][0]["number"],
    }
    # store the result in a pandas dataframe and write to a parquet file
    df4 = pd.DataFrame(result, index=[0])
    df4.to_parquet("data/output/sms_result.parquet")


except Exception as e:
    print(f"An error occurred: {str(e)}")
    