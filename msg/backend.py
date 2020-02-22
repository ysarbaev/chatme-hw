import kafka
import conf
import signal
import threading

consumer = kafka.KafkaConsumer(
	conf.kafka['topic'],
	bootstrap_servers=conf.kafka['bootstrap_servers'],
	group_id='backend',
	value_deserializer=conf.kafka['value_deserializer']
)

INTERRUPT_EVENT = threading.Event()

def stop(signum, frame):
	consumer.close(False)
	exit(0)

def listen_kill_server():
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGQUIT, stop)
    signal.signal(signal.SIGHUP, stop)

listen_kill_server()

for message in consumer:
	print(message.value)
