#!/bin/bash

# Kill existing containers first
bash -x ./stop_server.sh

# Then bring them up
docker-compose --file=docker-compose.yml up --build -d --remove-orphans --force-recreate