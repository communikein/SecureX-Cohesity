from flask import Flask, request, jsonify
import requests
import os

securex_url = 'https://securex-ao.eu.security.cisco.com'

# get environment variables
WT_BOT_TOKEN = os.environ['WT_BOT_TOKEN']
WT_BOT_EMAIL = os.environ['WT_BOT_EMAIL']
SECUREX_TOKEN = os.environ['SECUREX_TOKEN']
SECUREX_WEBHOOK_ID = os.environ['SECUREX_WEBHOOK_ID']

# start Flask and WT connection
app = Flask(__name__)

@app.route('/', methods=['POST'])
def action_received(action, request):
    raw_json = request.get_json()
    print(raw_json)

    personEmail_json = raw_json['data']['personEmail']
    room_id = raw_json['data']['roomId']
    message = str(raw_json) #'Got it! Command received :)'
    attachment = ''

    if personEmail_json != WT_BOT_EMAIL:
        args = {
            'api_key': SECUREX_TOKEN
        }
        payload = {
            'action': action,
            'room_id': room_id,
            'bot_token': WT_BOT_TOKEN,
            'message': message,
            'attachment': attachment
        }
        response = requests.post(securex_url + '/webhooks/' + SECUREX_WEBHOOK_ID, params=args, data=payload)
        
    return jsonify({'success': True})

if __name__=="__main__":
    app.run()