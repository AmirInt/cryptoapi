# Cryptoapi

The project provides an API to get different cryptocurrency values against USD.


## Project Phases

This project consists of three phases:

1. The first phase simply is an image of a **curl-enabled alpine** in Docker.
2. The second phase developes our server based on **fastapi** and deploys it along with its custom configurations onto Docker. This phase uses Redis (image: redislabs/redismod) as a database to hold the currencies values temporarily for a configurable amount of time, and prevent excess requests to the API server.
3. The third phase simulates the project on a Kubernetes cluster with 2 replicas of the server, 1 of the database and 1 client. The client uses the image deployed in the first phase. Such characteristics are of course arbitrary and configurable.