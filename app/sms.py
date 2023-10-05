from twilio.rest import Client

# Your Twilio Account SID and Auth Token
account_sid = 'ACb1f8718e01bcc3eacf727272ff3a7b2b'
auth_token = 'e89d5fb009283196464e6ed7faf8bd88'

# Create a function to send SMS messages
def send_sms(numbers_to_message, message_body):
    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Your Twilio phone number (this is the number you purchased on Twilio)
    from_phone_number = '+18023289660'

    for number in numbers_to_message:
        message = client.messages.create(
            from_=from_phone_number,
            body=message_body,
            to=number
        )

        print(f"Message SID for {number}: {message.sid}")
