from flask import Flask, request #самоссылки
import logging
import json
from dialogs import hello_dialog

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/post', methods=['POST'])
def main():

    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    
    hello_dialog(response, request.json)
   
    logging.info('Request: %r', response)

    return json.dumps(response)


if __name__ == '__main__':
    app.run()
