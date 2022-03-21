from datetime import datetime, timedelta
import os

import jwt
from clients.DbClient import DbClient

class UsersService (object):
    __JWT_KEY = os.environ.get("JWT_KEY")
    
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(UsersService, self).__new__(self)
        return self.instance

    def get_token(self, user_id, user_password):
        user = DbClient.get_user(user_id, user_password)
        token = None
        if user is not None:
            token = jwt.encode({
                'id': user.id,
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, self.__JWT_KEY)
        return token
        