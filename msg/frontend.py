import os
import flask as f
import kafka
import conf
import json
import time

def create_app(test_config=None):
    app = f.Flask(__name__, instance_relative_config=True)

    producer = create_producer()

    @app.route('/', methods=['GET'])
    def render_form():
        return f.render_template('post-message.html')

    @app.route('/', methods=['POST'])
    def handle_message():
        message = f.request.form['message']
        validated = validate(message)
        if validated[0]:
            send(f.request.remote_addr, message, producer)
            return ""
        else:
            return validated[2]

    return app
    

def send(ip, message, producer):
    data = {'data': message, 'time': time.time()}
    producer.send(conf.kafka['topic'], key=ip, value=data)


def create_producer(): 
    p = kafka.KafkaProducer(
        bootstrap_servers=conf.kafka['bootstrap_servers'],
        value_serializer=conf.kafka['value_serializer'],
        key_serializer=conf.kafka['key_serializer'])
    return p


def validate(message):
    max_len = conf.limits['max_message_size']
    if message == None:
        return (False, 'message.empty', None)
    elif len(message) > max_len:
        return (False,
            'message.size_exceeded',
            'Max message size is %s' % max_len)
    else:
        return  (True, None, None)
           