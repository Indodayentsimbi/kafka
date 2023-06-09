from schemas import customer

def dict_to_obj(customer_dict, ctx):
    """
    Receives a dictionary and converts back to customer object
    """
    return customer(customer_dict["id"],customer_dict["name"],customer_dict["surname"],customer_dict["age"])


def callback(consumer, partitions):
    for p in partitions:
        print(f'Assigned to {p.topic}, partition {p.partition}')


def func_consumer(consumer,topics,callback):
    """
    This function takes as input the following:
    consumer -> The instance of the consumer class
    topics -> A list of topics
    callback -> Callback function    
    """
    try:
        consumer.subscribe(topics,on_assign=callback)
    except Exception as e:
        print(e)    