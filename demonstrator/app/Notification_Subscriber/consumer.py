import json
import sys

import pika
import requests

FROST_SERVER = "http://192.168.1.148:8080/FROST-Server/"
url = '192.168.1.148'
params = pika.ConnectionParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel
channel.queue_declare(queue='notify_queue_1', durable=True)


def process_payload(body):
    # Code to post the data to the FROST_SERVER go here
    data_str = body.decode('utf-8').replace("'", '"')

    # Convert the bytearray body into json
    data = json.loads(data_str)
    print(" [x] Received: %r" % data)


    url = FROST_SERVER + '/v1.1/Observations'
    observation = {
        "phenomenonTime": data['record']['time'],
        "resultTime": data['record']['time'],
        "result": data['record']['value'],
        "FeatureOfInterest": {
            "name": data['record']['metric'],
            "description": "PairTree",
            "encodingType": "application/vnd.geo+json",
            "feature": {
                "type": "Point",
                "coordinates": [
                    data['record']['latitude'],
                    data['record']['longitude']
                ]
            }
        },
        "Datastream": {
            "@iot.id": data['record']['oem_sensor_id']
        }
    }


    response = requests.post(url=url, json=observation)
    print(response)


def main():
    def callback(ch, method, properties, body):
        process_payload(body)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='notify_queue_1', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    print(' [*] Waiting for message. To exit press Command+C')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        connection.close()
        sys.exit()
