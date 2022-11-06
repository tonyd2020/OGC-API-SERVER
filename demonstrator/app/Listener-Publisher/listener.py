import psycopg3, json, requests
import pika

conn = psycopg3.connect(host="192.168.1.148", port=5430, dbname="pairtree", user="team6", password="ITC303", autocommit=True)
conn.cursor().execute("LISTEN sample_changed")

pika_connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.148'))
channel = pika_connection.channel()
channel.queue_declare(queue='notify_events', durable=True)

gen = conn.notifies()
for notify in gen:
    payload = notify.payload
    data = f"{json.loads(payload)}"
    owner_id =int(json.loads(payload)['record']['owner_id'])
    channel.basic_publish(exchange='', routing_key=f'notify_queue_{owner_id}', body=data, properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    print(data)
