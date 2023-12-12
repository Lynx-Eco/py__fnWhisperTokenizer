# create the network for the mqtt bus
docker network create mqtt_network

# run the `emqx/emqx` container on that network.
docker run -d --name emqx --network mqtt_network -p 1883:1883 -p 18083:18083 emqx/emqx:latest

# run our python client container on that network also.
docker run --network mqtt_network nargetdev/local-agreement


#TODO: merge this into a compose file.