"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from flask import Flask, request, jsonify
import requests
from webexteamssdk import WebexTeamsAPI
import os

securex_url = 'https://securex-ao.eu.security.cisco.com'

# get environment variables
WT_BOT_TOKEN = os.environ['WT_BOT_TOKEN']
WT_BOT_EMAIL = os.environ['WT_BOT_EMAIL']
SECUREX_TOKEN = os.environ['SECUREX_TOKEN']
SECUREX_WEBHOOK_ID = os.environ['SECUREX_WEBHOOK_ID']

# start Flask and WT connection
app = Flask(__name__)
api = WebexTeamsAPI(access_token=WT_BOT_TOKEN)

# defining the decorater and route registration for incoming alerts
@app.route('/', methods=['POST'])
def alert_received():
    raw_json = request.get_json()
    print(raw_json)

    # customize the behaviour of the bot here
    message = "Hi, I am a Webex Teams bot. Have a great day ☀! "

    WT_ROOM_ID = raw_json['data']['roomId']
    personEmail_json = raw_json['data']['personEmail']
    if personEmail_json != WT_BOT_EMAIL:
        requests.get(securex_url + '/webhooks/' + SECUREX_WEBHOOK_ID + '?api_key=' + SECUREX_TOKEN)
        api.messages.create(roomId=WT_ROOM_ID, markdown=message)
    
    return jsonify({'success': True})

if __name__=="__main__":
    app.run()