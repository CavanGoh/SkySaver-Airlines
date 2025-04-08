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

### 2. Start Backend Services

```bash
# Start microservices
cd backend
docker compose up
```

### 3. Start Frontend

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
