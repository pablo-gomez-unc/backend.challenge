class LoggingService:
    __logger = None
    
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(LoggingService, self).__new__(self)
        return self.instance
    
    def get_logger(self):
        return self.__logger
    
    def set_logger(self,logger):
        self.__logger = logger 