from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from utils import func_producer,delivery_report,obj_to_dict 
from schemas import customer
import random
import os
from time import sleep
import argparse

# This commandline args are only required when running from outside the container
parser = argparse.ArgumentParser()
parser.add_argument("--bootstrap_servers",type=str)
parser.add_argument("--topic",type=str)
args = parser.parse_args()

acks = os.environ.get("ACKS","all")
idempotency = os.environ.get("ENABLE_IDEMPOTENCE",True)
servers = os.environ.get("BOOTSTRAP_SERVERS",args.bootstrap_servers)
client = os.environ.get("CLIENT_ID","unkown")
topic = os.environ.get("TOPIC",args.topic)

config = {"acks":acks,
          "client.id":client,
          "enable.idempotence":idempotency,
          "bootstrap.servers":servers}


if __name__ == "__main__":
    producer = Producer(config)
    schema_client = SchemaRegistryClient(conf={"url":"http://schema-registry:8081"}) # change to localhost:8081 when running locally
    schema = schema_client.get_schema(schema_id=5)     
    serializer = JSONSerializer(schema_str=schema,
                                schema_registry_client=schema_client,
                                to_dict=obj_to_dict,
                                conf={"auto.register.schemas":False})
    i = 1
    while i < 100 :
        name = "".join(random.choices(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],k=random.randint(4,15)))
        surname = "".join(random.choices(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],k=random.randint(4,15)))
        customer_inst = customer(id=i,name=name,surname=surname,age=random.randint(18,50),gender=random.choice(["male","female","other"]))
        val = serializer(obj=customer_inst,ctx=SerializationContext(topic,MessageField.VALUE))
        func_producer(producer=producer,
                      topic=topic,
                      value= val,
                      key=str(customer_inst.id),
                      callback=delivery_report) 
        i += 1
        sleep(5)
    producer.flush()                      

