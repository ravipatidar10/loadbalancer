#!/bin/bash

docker compose down
pip install matplotlib
pip install requests

docker compose -f docker-compose-single-server.yml up -d
sleep 5
python goodput.py 8000 > single_server_data.csv

ALGO=$(grep "^ALGO=" .env | cut -d '=' -f 2-)


docker compose down
sed -i "s/^ALGO=.*/ALGO=round_robin/" .env
docker compose up -d
sleep 5
python goodput.py 5000 > loadbalancer_round_robin.csv

sed -i "s/^ALGO=.*/ALGO=least_connection/" .env
docker compose up -d
sleep 5
python goodput.py 5000 > loadbalancer_least_connection.csv

python scaling_data.py > scaling_data.csv

python graph.py
sed -i "s/^ALGO=.*/ALGO=$ALGO/" .env