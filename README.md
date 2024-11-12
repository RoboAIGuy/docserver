# DocServer - Document management Engine

This repository contains Python webserver containing a FastAPI engine to create and manage documents.


## Overview
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
- [Usage](#usage)
- [APIs](#APIs)
- [Backend](#Backend)

### Pre-requisites

- Install Docker with Docker Desktop


### Installation

1. Clone the repository to your local machine.
2. Create a empty 'POSTGRESDATA' directory inside the cloned directory.


### Usage

- Run Docker Engine
- Open terminal/cmd
- Create a Docker Network
  ```bash
  docker network create docnetwork
  ```

- Run the containers
  ```bash
  docker-compose up -d --build
  ```

- To get into the Swagger docs open the following in your browser '0.0.0.0:8000/docs'

- To run tests use the following command
  ```bash
  docker exec -it docserver_app pytest app/tests/
  ```



### Backend

- Framework: FastAPI
- Database: PostgreSQL
- API Documentation: Swagger
- API Type: RESTful

