from confluent_kafka import Consumer, KafkaException
from utils import func_consumer,callback 
import os
import argparse

# This commandline args are only required when running from outside the container
parser = argparse.ArgumentParser()
parser.add_argument("--bootstrap_servers",type=str)
parser.add_argument("--topic",type=str)
parser.add_argument("--group_id",type=str)
args = parser.parse_args()

auto_commit = os.environ.get("ENABLE_AUTO_COMMIT",False)
isolation_level = os.environ.get("ISOLATION_LEVEL","read_committed")
auto_offset = os.environ.get("AUTO_OFFSET_RESET","earliest")
servers = os.environ.get("BOOTSTRAP_SERVERS",args.bootstrap_servers)
group_id = os.environ.get("GROUP_ID",args.group_id)
topic = os.environ.get("TOPIC",args.topic)

config = {"group.id":group_id,
          "auto.offset.reset":auto_offset,
          "enable.auto.commit":auto_commit,
          "bootstrap.servers":servers,
          "isolation.level":isolation_level}


if __name__ == "__main__":
    consumer = Consumer(config)  
    try:
        func_consumer(consumer=consumer,topics=[topic],callback=callback) 
        while True:
            event = consumer.poll(1)
            if event is None:
                continue
            elif event.error():
                raise KafkaException(event.error())
            else:
                val = event.value().decode("utf8")
                partition = event.partition()
                print("Received: {} from partition {}".format(val,partition)) 
                consumer.commit(event)     
    except KeyboardInterrupt:
        print("Cancelled by user")
    finally:
        consumer.close()                         

