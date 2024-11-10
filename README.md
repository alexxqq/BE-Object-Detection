# BE-Object-Detection

This repository contains the backend for the **Object Detection** project, built using **FastAPI** and Docker Compose for easy setup and deployment.

## Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/get-started) (for running Docker containers)

## Setup

### 1. Clone the repository

Start by cloning the repository to your local machine:

```bash
git clone git@github.com:alexxqq/BE-Object-Detection.git
cd BE-Object-Detection
```
### 2. Create .env (if needed)
```bash
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
DB_USER=
DB_HOST=
DB_PASS=
DB_PORT=
```
### 3. Build and run the containers

Once inside the project directory, use Docker Compose to build and start the containers:

```bash
docker-compose up --build
```
### 4. Access the FastAPI Application

After the containers are up and running, you can access the FastAPI backend:

```bash
http://localhost:8000/docs
```


