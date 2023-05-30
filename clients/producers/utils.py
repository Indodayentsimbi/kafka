def callback(err, event):
    if err:
        print(f'Produce to topic {event.topic()} failed for event: {event.key()}')
    else:
        val = event.value().decode('utf-8')
        print(f'{val} sent to partition {event.partition()}.')


def func_producer(producer,topic,value,key,callback):
    """
    This function takes as input the following:
    producer -> The instance of the producer class
    topic -> The created topic to send events too
    value -> The event payload
    key -> To be hashed and automatically go to the correct partition
    callback -> Callback function
    """         
    try:
        producer.produce(topic=topic,value=value,key=key,on_delivery=callback)
    except Exception as e:
        print(e)        