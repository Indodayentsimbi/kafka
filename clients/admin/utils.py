from confluent_kafka import KafkaException
from confluent_kafka.admin import NewTopic, ConfigResource


def topic_exists(admin, topic):
    try:
        metadata = admin.list_topics()
        for t in iter(metadata.topics.values()):
            if t.topic == topic:
                return True
        return False        
    except KafkaException:
        raise "Error retrieving topics"


def create_topic(admin, topic, partitions, replication):
    try:
        new_topic = NewTopic(topic=topic,num_partitions=partitions,replication_factor=replication)
        result = admin.create_topics([new_topic])
        for topic, future in result.items():
            try:
                future.result()
                print("Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create topic {}: {}".format(topic,e))    
    except KafkaException:
        raise "Error creating new topic"


def describe_topic(admin, topic):
    try:
        resource = ConfigResource(restype="topic",name=topic)
        result = admin.describe_configs(resource=[resource])
        config_dict = result.get(resource,{}).result()
        return config_dict
    except KafkaException:
        raise "Error retrieving topic configuration"


# def set_max_size(admin, topic, max_k):
#     config_dict = {'max.message.bytes': str(max_k*1024)}
#     resource = ConfigResource('topic', topic, config_dict)
#     result_dict = admin.alter_configs([resource])
#     result_dict[resource].result()