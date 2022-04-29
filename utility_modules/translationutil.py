import requests
import uuid
import json
import os

from .myloggerutil import MyLoggerUtil

class TranslationUtil:

    def __init__(self) -> None:
        self.mylogger = MyLoggerUtil(__name__).logger
        self.apikey = os.getenv('AZURE_TRAN_KEY')
        self.api_endpt = os.getenv('AZURE_ENDP') + 'translate'
        self.api_loc = os.getenv('AZURE_LOC')

    '''
    translate function takes in original msg and the language code to 
    translate to and return the translated message.
    '''
    def translate(self, msg : str, lang_code : str) -> str :

        headers = {
            'Ocp-Apim-Subscription-Key': self.apikey,
            'Ocp-Apim-Subscription-Region': self.api_loc,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        params = {
            'api-version': '3.0',
            'to': [lang_code]
        }

        body = [{
            'text': msg
        }]

        self.mylogger.info(f'Sent POST request to endpoint: {self.api_endpt}')
        request = requests.post(self.api_endpt, params=params, headers=headers, json=body)
        if request.status_code == 200:
            self.mylogger.info('POST request returns successfully.')
            resp = request.json()

            translate_result_obj = resp[0].get('translations')
            translate_result = translate_result_obj[0].get('text')
            return translate_result
        else:
            self.mylogger.error(f'{lang_code}')
            self.mylogger.error(f'POST request failed: status_code={request.status_code} - {request.reason}')
            return None

if __name__ == '__main__':
    translate_svc = TranslationUtil()
    result = translate_svc.translate('hello world!', 'korean')
    print(result)
    
