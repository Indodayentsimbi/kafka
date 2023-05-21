# Build docker image for kafka

docker build -t kafka-img:v1 .

# Build docker image for zookeeper

docker build -t zookeeper-img:v1 .

# Build docker network

docker network create kafka

# Run zookeeper container

docker run -d -t --env-file ./.env --name zookeeper --net kafka zookeeper-img:v1

# Run kafka container

docker run -d -t --env-file ./.env --name broker_1 --net kafka kafka-img:v1