from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

class MessageRequest(BaseModel):
    to_phone_number: str
    message_body: str

@app.post('/send_message')
def send_message(message_request: MessageRequest):
    try:
        # Send the message using Twilio API
        message = client.messages.create(
            body=message_request.message_body,
            from_=twilio_phone_number,
            to=message_request.to_phone_number
        )
        # Return success message
        return {'message': 'Message sent successfully.', 'message_sid': message.sid}
    except Exception as e:
        # Return error message if sending fails
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
