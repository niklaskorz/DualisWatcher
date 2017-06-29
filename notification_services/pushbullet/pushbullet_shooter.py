class PushbulletShooter(object):
    """
    Encapsulates the sending of pushbullet pushes.
    """
    def __init__(self, access_token: str):
        self.access_token = access_token

    