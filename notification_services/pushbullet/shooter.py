import json
from http.client import HTTPSConnection, HTTPResponse

class PushbulletShooter(object):
    """
    Encapsulates the sending of pushbullet pushes.
    """
    def __init__(self, access_token: str):
        self.connection = HTTPSConnection('api.pushbullet.com')
        self.token = access_token
    
    def close(self):
        self.connection.close()

    def verify(self):
        self.connection.request(
            'GET',
            '/v2/users/me',
            headers={
                'Access-Token': self.token
            }
        )

        response = self.connection.getresponse()
        response.read()
        return response.getcode() == 200

    def send(self, data):
        self.connection.request(
            'POST',
            '/v2/pushes',
            body=json.dumps(data),
            headers={
                'Access-Token': self.token,
                'Content-Type': 'application/json'
            }
        )

        response = self.connection.getresponse()
        response.read()
        return response.getcode() == 200

    def send_note(self, title, body):
        self.send({ 'type': 'note', 'title': title, 'body': body })
    