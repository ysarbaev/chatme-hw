import json

kafka = {
	'bootstrap_servers': ['localhost:9092'],
	'topic': 'messages',
	'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
	'value_deserializer': lambda m: json.loads(m.decode('utf-8')),
	'key_serializer': lambda k: bytes(k, 'utf-8')
}

limits = {
	'max_message_size': 8
}
