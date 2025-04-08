Collecting workspace information# SkySaver Airlines

A full-stack airline booking system with microservices architecture, featuring standard booking, flexible booking options, and real-time notifications for discounted flights.

## Project Overview

SkySaver Airlines is a web application that offers:
- Standard flight booking
- SmartFlex booking with discounted pricing
- Real-time notifications for seat availability
- Flight cancellation with automatic notification system
- Payment processing integration


## Prerequisites

- [WampServer](https://www.wampserver.com/) (for MySQL databases)
- [Python 3.x](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/)

## Setup Instructions

### 1. Start WAMP

### 2. Import database from SQL files
Import the SQL files under MYSQL files
1. flexSeat.sql
2. user.sql
3. booking.sql
4. notification.sql
5. seat.sql
6. payment.sql

### 2. Setup RabbitMQ
```bash
cd backend
docker build -t skysaver-rabbitmq .
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 skysaver-rabbitmq
python rabbit_setup.py
```

### 3. Start Backend Services

```bash
# For each of the cd below, open a new terminal before executing 
# Start flexseat service 
cd backend
cd atomicMicroservices
cd flex User
python flexseat.py

# Start notification service 
cd backend
cd atomicMicroservices
cd notification
python notification.py

# Start payment service 
cd backend
cd atomicMicroservices
cd payment
docker build -t paymentservice .
docker run -p 5005:5005 payment-service

# Start BookingCancelled composite service 
cd backend
cd compositeMicroservices
python BookingCancelled.py

# Start NotifyFlexUsers composite service 
cd backend
cd compositeMicroservices
python NotifyFlexUSers.py

#Run the other services
cd backend
docker compose up
```

### 4. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Once started, the frontend will be available at http://localhost:5173


## Directory Structure

- frontend: Vue.js frontend application
- backend: Python backend services
  - `/atomicMicroservices`: Individual microservices
  - `/compositeMicroservices`: Services that coordinate multiple atomic services

##To test, register 2 accounts. 

#To test payment, use Paypal sandbox account given below:
sb-dqk6w31792637@personal.example.com
!QVp@7x4
