from flask import Flask,request,jsonify
from flask_cors import CORS
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
app= Flask(__name__)
CORS(app)

client= Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

@app.route('/send_sos',methods= ['POST'])
def send_sos():
    data=request.json
    lat, lon = data.get("latitude"), data.get("longitude")
    
    if not lat or not lon:
        return jsonify({"error" : "location not provided"}), 400
    
    message= f"🚨 EMERGENCY! Need help at location: https://maps.google.com/?q={lat},{lon}"
    
    try:
        msg = client.messages.create(
            body= message,
            from_=os.getenv("TWILIO_PHONE"),
            to= os.getenv("EMERGENCY_CONTACT")
            
        )
        return jsonify({"status": "sent", "sid": msg.sid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
