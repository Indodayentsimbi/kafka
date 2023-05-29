from confluent_kafka import Producer
from producer_A.producer import func_producer
from util import callback 
import os
from time import sleep
import argparse

# This commandline args are only required when running from outside the container
parser = argparse.ArgumentParser()
parser.add_argument("--bootstrap_servers",type=str)
parser.add_argument("--topic",type=str)
args = parser.parse_args()

acks = os.environ.get("ACKS","all")
idempotency = os.environ.get("ENABLE_IDEMPOTENCY",True)
servers = os.environ.get("BOOTSTRAP_SERVERS",args.bootstrap_servers)
client = os.environ.get("CLIENT_ID","unkown")
topic = os.environ.get("TOPIC",args.topic)

config = {"acks":acks,
          "client.id":client,
          "enable.idempotence":idempotency,
          "bootstrap.servers":servers}


if __name__ == "__main__":
    producer = Producer(config)     
    i = 1
    while i < 100 :
        func_producer(producer=producer,
                      topic=topic,
                      value= str(i),
                      key=str(i),
                      callback=callback) 
        i += 1
        sleep(5)
    producer.flush()                      

