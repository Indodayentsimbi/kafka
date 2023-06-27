from confluent_kafka.admin import AdminClient
from utils import topic_exists,create_topic,describe_topic
import argparse
import os

# This commandline args are only required when running from outside the container
parser = argparse.ArgumentParser()
parser.add_argument("--bootstrap_servers",type=str)
parser.add_argument("--topic",type=str)
args = parser.parse_args()

servers = os.environ.get("BOOTSTRAP_SERVERS",args.bootstrap_servers)
topic = os.environ.get("TOPIC",args.topic)

config = {"bootstrap.servers":servers}


if __name__ == "__main__":
    admin = AdminClient(conf=config)

    # Create topic if not exists:
    if not topic_exists(admin=admin,topic=topic):
        create_topic(admin=admin,topic=topic,partitions=3,replication=1)

    print(describe_topic(admin=admin,topic=topic))    
