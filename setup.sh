#!/bin/bash

# Navigate to the frontend directory
cd frontend

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Build the frontend (optional)
echo "Building frontend..."
npm run build

# Navigate back to the root directory
cd ..

# Navigate to the backend directory
cd backend

# Create a virtual environment (optional)
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Run database migrations (if any)
# echo "Running database migrations..."
# flask db upgrade

# Start the backend server
echo "Starting backend server..."
flask run &

# Navigate back to the frontend directory and start the frontend server
cd ../frontend
echo "Starting frontend server..."
npm start

echo "Setup complete. Frontend running on http://localhost:3000 and backend running on http://localhost:5000"
