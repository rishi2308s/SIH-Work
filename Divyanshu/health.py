import json
from twilio.rest import Client as twilio_client
import requests
from dotenv import load_dotenv, find_dotenv
import os
message_client = None
twilio_phone_number = None
delivery_phone_number = None
load_dotenv(find_dotenv())
# api_key = os.getenv("API_KEY")
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
delivery_phone_number = "+918800120452"
message_client = twilio_client(twilio_account_sid, twilio_auth_token)
def calculate_conveyor_health(num_holes, avg_hole_size, avg_thinning):
    N_crit = 5       # Critical number of holes
    S_crit = 50      # Critical average hole size
    T_crit = 30      # Critical average thinning (%)

    # Weights (assuming equal impact)
    W_S = 0.38
    W_N = 0.35
    W_T = 0.27

    # Calculate health index
    health_index = 100 - (
        (min(num_holes / N_crit, 1) * W_N) +
        (min(avg_hole_size / S_crit, 1) * W_S) +
        (min(avg_thinning / T_crit, 1) * W_T)
    ) * 100

    return max(health_index, 0)  # Ensure health doesn't go below 0

# Example usage
num_holes = 6
avg_hole_size = 20
avg_thinning = 10
if (num_holes>5):
    message = message_client.messages.create(
        from_= twilio_phone_number,
        body = "TOO MANY HOLES!!",
        to = delivery_phone_number
    )
elif (avg_hole_size>50):
    message = message_client.messages.create(
        from_= twilio_phone_number,
        body = "Too big holes!!!!",
        to = delivery_phone_number
    )
elif (avg_thinning>30):
    message = message_client.messages.create(
        from_= twilio_phone_number,
        body = "TOO MUCH EROSION!!",
        to = delivery_phone_number
    )
health_status = calculate_conveyor_health(num_holes, avg_hole_size, avg_thinning)
print(f"Conveyor Belt Health: {health_status}%")
