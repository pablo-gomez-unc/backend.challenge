import os
import jwt

from datetime import datetime, timedelta
from services.LoggingService import LoggingService
from clients.DbClient import DbClient

class UserAuthService (object):
    __JWT_KEY = os.environ.get("JWT_KEY")
    __TOKEN_EXPIRATION_MINUTES =  int(os.environ.get("TOKEN_EXPIRATION_MINUTES"))
    
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(UserAuthService, self).__new__(self)
        return self.instance

    def get_token(self, user_id, password) -> str:
        user = DbClient().get_user(user_id, password)
        if user == {}:
            return None
        
        token = jwt.encode({
                'user_id': user.get('user_id'),
                'exp' : datetime.utcnow() + timedelta(minutes = self.__TOKEN_EXPIRATION_MINUTES)
                }, self.__JWT_KEY
        )
            
        return token
        
    def is_token_valid(self,token) -> bool:
        try:
            data = jwt.decode(token, self.__JWT_KEY, algorithms=['HS256'])
            LoggingService().get_logger().debug(DbClient().get_user_list())

            if data.get('user_id') not in [user['user_id'] for user in DbClient().get_user_list()]:
                raise Exception("User associated with access token is not longer valid")
            return True
        
        except jwt.ExpiredSignatureError:   
            LoggingService().get_logger().error("Invalid token: Token has expired")
            return False
        
        except Exception as e:
            LoggingService().get_logger().error("Invalid token: " + str(e))
            return False    
        