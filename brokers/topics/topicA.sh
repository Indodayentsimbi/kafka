kafka-topics --bootstrap-server broker-1:29091,localhost:9091 --topic topicA --partitions 3 --replication-factor 1 --if-not-exists --create