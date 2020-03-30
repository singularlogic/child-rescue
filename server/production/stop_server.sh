#!/bin/bash

# Kill existing containers first
docker-compose --file=docker-compose.yml down --remove-orphans
