from confluent_kafka import Consumer, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import SerializationContext,MessageField
from utils import func_consumer,callback,dict_to_obj
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

MIN_COMMIT_COUNT = 30

if __name__ == "__main__":
    consumer = Consumer(config)
    schema_client = SchemaRegistryClient(conf={"url":"http://localhost:8081"}) # change to localhost:8081 when running locally
    schema = schema_client.get_schema(schema_id=5)
    deserializer = JSONDeserializer(schema_str=schema,from_dict=dict_to_obj,schema_registry_client=schema_client)
    try:
        func_consumer(consumer=consumer,topics=[topic],callback=callback) 
        # an event has the following atributes: topic(),partition(),value(),key(),error(),offset(),headers(),timestamp()
        event_cnt = 0
        while True:
            event = consumer.poll(1)
            if event is None:
                continue
            elif event.error():
                raise KafkaException(event.error())
            else:
                event_cnt += 1
                # val = event.value().decode("utf-8")
                # partition = event.partition()
                # print("Received: {} from partition {} on topic {}".format(val,partition,event.topic()))
                print(event.value())
                customer = deserializer(data=event.value(),ctx=SerializationContext(topic,MessageField.VALUE))
                if customer is not None:
                    print(customer)
                ### HERE YOU CAN CALL ANOTHER FUNCTION TO PROCESS THE EVENT ###
                
                # Use this method to commit offsets if you have ‘enable.auto.commit’ set to False
                
                consumer.commit(message=event,asynchronous=True) # this returns None

                ## OR ##

                # if event_cnt % MIN_COMMIT_COUNT == 0:
                #     consumer.commit(message=event,asynchronous=False) # this returns TopicPartition              
    except KeyboardInterrupt:
        print("Cancelled by user")
    finally:
        # trigger a group rebalance which ensures that any partitions owned by the consumer gets re-assigned to another member in the group
        consumer.close()                         

