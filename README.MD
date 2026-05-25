# SANGOKU - A Mini FaaS Platform

A lightweight Function-as-a-Service (FaaS) platform built using:

* Python Flask
* Docker
* MySQL
* Docker Volumes
* Dynamic Runtime Detection

The platform supports:

* Python functions
* Node.js functions
* ZIP project uploads
* Multi-function deployments
* Dynamic function invocation
* Persistent source code storage
* Metadata registry using MySQL

---

# Architecture Overview

```text
Client
   |
   v
Flask Gateway
   |
   |-- Upload Function
   |-- Normalize Upload
   |-- Detect Runtime
   |-- Build Docker Image
   |-- Save Metadata
   |
   v
Docker Runtime

MySQL -> Function Metadata
Docker Volume -> Source Storage
```

---

# Project Structure

```text
mini-faas/
│
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
│
├── gateway/
│   ├── builder.py
│   ├── database.py
│   ├── detector.py
│   ├── extractor.py
│   ├── normalizer.py
│   ├── parser.py
│   ├── runner.py
│   │
│   └── templates/
│       ├── python.Dockerfile
│       └── node.Dockerfile
│
├── mysql/
│   └── init.sql
│
├── build/
│
└── examples/
```

---

# Core Components

## Flask Gateway

The Flask gateway acts as the API entrypoint.

Responsibilities:

* Receive uploads
* Normalize projects
* Build Docker images
* Invoke deployed functions
* Communicate with MySQL

Main endpoints:

| Endpoint                             | Description                |
| ------------------------------------ | -------------------------- |
| POST /deploy                         | Deploy a function          |
| POST /invoke/<deployment>/<function> | Invoke a deployed function |
| GET /                                | Health check               |

---

## Docker Images

Each uploaded function is converted into its own Docker image.

Example:

```text
faas_addition
```

This isolates execution environments between functions.

---

## MySQL Metadata Registry

MySQL stores:

* deployment names
* runtime types
* image names
* function entrypoints

Tables:

### functions

| Column     | Description       |
| ---------- | ----------------- |
| id         | Primary key       |
| name       | Deployment name   |
| runtime    | Runtime type      |
| image      | Docker image name |
| created_at | Timestamp         |

### function_entrypoints

| Column        | Description       |
| ------------- | ----------------- |
| id            | Primary key       |
| function_id   | Linked deployment |
| function_name | Function name     |
| entrypoint    | Python entrypoint |

---

## Docker Volumes

### sangoku

Persistent storage for uploaded source code.

Mounted to:

```text
/app/functions
```

### sangoku_metadata

Persistent MySQL database storage.

Mounted to:

```text
/var/lib/mysql
```

---

# Upload Flow

```text
1. Client uploads file
2. Flask receives upload
3. normalizer.py processes upload
4. Source code saved to Docker volume
5. Source copied into build workspace
6. Runtime detected
7. Docker image built
8. Metadata saved to MySQL
9. Deployment ready for invocation
```

---

# Invocation Flow

```text
1. Client invokes function
2. runner.py queries MySQL
3. Docker image retrieved
4. Entrypoint resolved
5. Docker container executed
6. Function result returned
```

---

# Supported Upload Types

| Upload Type                    | Supported |
| ------------------------------ | --------- |
| Single Python File             | Yes       |
| Single Node.js File            | Yes       |
| ZIP Project                    | Yes       |
| Multiple Functions in One File | Yes       |

---

# Example Python Function

```python
def add(event):

    a = event.get("a")
    b = event.get("b")

    return {
        "result": a + b
    }


def subtract(event):

    a = event.get("a")
    b = event.get("b")

    return {
        "result": a - b
    }
```

---

# Deployment Example

## Endpoint

```http
POST /deploy
```

## Form Data

| Field | Value      |
| ----- | ---------- |
| name  | addition   |
| file  | handler.py |

---

# Invocation Example

## Add Function

### Endpoint

```http
POST /invoke/addition/add
```

### Request Body

```json
{
  "a": 10,
  "b": 5
}
```

### Response

```json
{
  "result": 15
}
```

---

## Subtract Function

### Endpoint

```http
POST /invoke/addition/subtract
```

### Request Body

```json
{
  "a": 10,
  "b": 5
}
```

### Response

```json
{
  "result": 5
}
```

---

# Docker Compose

```yaml
services:

  gateway:

    image: faas_gateway

    build: .

    ports:
      - "5000:5000"

    volumes:
      - sangoku:/app/functions
      - ./build:/app/build
      - /var/run/docker.sock:/var/run/docker.sock

    depends_on:
      - mysql

  mysql:

    image: mysql:8

    restart: always

    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: faas_db

    ports:
      - "3307:3306"

    volumes:
      - sangoku_metadata:/var/lib/mysql
      - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql

  phpmyadmin:

    image: phpmyadmin/phpmyadmin

    restart: always

    ports:
      - "8080:80"

    environment:
      PMA_HOST: mysql
      PMA_PORT: 3306
      MYSQL_ROOT_PASSWORD: root

    depends_on:
      - mysql

volumes:

  sangoku:
    external: true

  sangoku_metadata:
    external: true
```

---

# Running the Platform

## Build and Start

```bash
docker compose up --build
```

---

## Stop Containers

```bash
docker compose down
```

---

## Remove Containers and Volumes

```bash
docker compose down -v
```

---

# Runtime Detection

The system automatically detects runtimes.

## Python Detection

Detected if project contains:

```text
.py files
```

## Node.js Detection

Detected if project contains:

```text
.js files
package.json
```

---

# Future Improvements

Potential upgrades:

* Async execution
* Hot containers
* Auto scaling
* Queue system
* Authentication
* API keys
* Function versioning
* Logging system
* Monitoring dashboard
* Cold start optimization
* Kubernetes integration
* GPU workloads
* WebAssembly runtimes

---

# Educational Concepts Demonstrated

This project demonstrates:

* Distributed systems
* Container orchestration
* Serverless architecture
* Dynamic code execution
* Runtime isolation
* Persistent volumes
* Metadata registries
* API gateway design
* Docker networking
* Multi-runtime environments

---

# Technologies Used

| Technology | Purpose             |
| ---------- | ------------------- |
| Flask      | API Gateway         |
| Docker     | Container Runtime   |
| MySQL      | Metadata Storage    |
| phpMyAdmin | Database Management |
| Python     | Runtime and Gateway |
| Node.js    | Additional Runtime  |

---

# Notes

* This project is intended for educational purposes.
* The current implementation executes untrusted code.
* Production-grade security isolation is not implemented.
* Resource limits and sandboxing should be added for real-world deployments.

---

# License

MIT License
