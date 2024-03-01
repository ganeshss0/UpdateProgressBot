from progress.utils import read_json, write_json, logging
from collections import namedtuple

class Response:
    def __init__(self, response_file:str) -> None:
        logging.info('Initializing Responses')
        
        self.AllResponse = read_json(response_file)
        self.create_response_instances()

    def create_response_instances(self):
        
        for response in self.AllResponse.keys():
            self.__setattr__(response, self.AllResponse[response])
        
    #def __repr__(self) -> dict:
       # return self.AllResponse
            
Response_Obj = namedtuple(
    'Response',
    [
        'introduction',
        'invalid_command',
        'help',
        'non_user_introduction'
    ]
)