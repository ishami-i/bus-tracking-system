#!/bin/bash

echo "⚠️ Removing old backend..."
rm -rf backend

echo "📁 Creating new backend structure..."

# Root
mkdir -p backend

# Core
mkdir -p backend/core/models
mkdir -p backend/core/repositories
mkdir -p backend/core/services

# API
mkdir -p backend/api/routes
mkdir -p backend/api/controllers

# Infrastructure
mkdir -p backend/infrastructure/database
mkdir -p backend/infrastructure/cache
mkdir -p backend/infrastructure/messaging

# Config
mkdir -p backend/config

# Tests
mkdir -p backend/tests

echo "📄 Creating __init__.py files..."

find backend -type d -exec touch {}/__init__.py \;

echo "📄 Creating starter files..."

# Core Models
touch backend/core/models/bus.py
touch backend/core/models/trip.py
touch backend/core/models/user.py

# Repositories
touch backend/core/repositories/bus_repository.py
touch backend/core/repositories/trip_repository.py

# Services
touch backend/core/services/bus_service.py
touch backend/core/services/trip_service.py

# API
touch backend/api/app.py
touch backend/api/routes/bus_routes.py
touch backend/api/routes/trip_routes.py
touch backend/api/controllers/bus_controller.py

# Infrastructure
touch backend/infrastructure/database/connection.py
touch backend/infrastructure/cache/redis_client.py
touch backend/infrastructure/messaging/mqtt_client.py

# Config
touch backend/config/settings.py

# Root files
touch backend/cli.py

echo "✅ Backend structure created successfully!"