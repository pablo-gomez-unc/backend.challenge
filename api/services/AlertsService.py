from clients.KafkaClient import KafkaClient

class AlertsService (object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(AlertsService, self).__new__(self)
        return self.instance
    
    def listen(self):
        return KafkaClient().listen()