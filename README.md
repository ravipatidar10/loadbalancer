
# Load Balancer

This project aims to create a load balancer system that dynamically scales up and scales down web servers based on incoming traffic. The load balancer distributes incoming requests among multiple servers replicas to ensure optimal performance and reliability.

## Running the Servers

To run the servers, use Docker Compose:

```bash
docker compose -d up
```

## Experiments and Graph Generation
```bash
python3 -m venv env
source env/bin/activate
bash experiments.sh 
```

