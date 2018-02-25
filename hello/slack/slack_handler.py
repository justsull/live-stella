import os
import json

class CommandHandler:

    def __init__(self, data):
        self.data = data
        self.command = self.data.get('command',None)
        self.token = self.data.get('token', None)
        self.url = self.data.get('text', None)
        self.response_url = self.data.get('response_url', None)
        self.slack_token = os.environ.get('VERIFICATION_TOKEN')

    def validate_request(self):
        request = True if self.token == self.slack_token else False
        return request

    @staticmethod
    def form_response(message):
        if type(message) is str:
            pass
        elif type(message) is dict: 
            message = json.dumps(message)
        response = {
            "response_type": "in_channel",
            "pretext": 'stella thinks the following general tags might work for your article:',
            "color": '#36a64f',
            "attachments": [
                {
                "text": message
                }
            ] 
            }
        return response