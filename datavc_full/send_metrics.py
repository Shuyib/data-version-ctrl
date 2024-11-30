"""this script reads the metrics.json file and sends the metrics to a phone number via SMS using the Africa's Taling API"""

import os
import sys
import json
import subprocess


def main():
    metrics_path = "metrics.json"

    # Check if metrics.json exists
    if not os.path.exists(metrics_path):
        print(f"Error: {metrics_path} does not exist.")
        sys.exit(1)

    # Read metrics from JSON file
    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    # Format the message
    message_lines = ["Model Metrics for insurance problem:"]
    for key, value in metrics.items():
        message_lines.append(f"{key}: {value}")
    message = "\n".join(message_lines)

    # Retrieve environment variables or provide defaults
    at_username = os.getenv("AT_USERNAME")
    phone_number = os.getenv("PHONE_NUMBER")

    # Send the message via send_sms.py
    try:
        subprocess.run(
            ["python3", "send_sms.py", at_username, phone_number, message], check=True
        )
        print("SMS sent successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error sending SMS: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
