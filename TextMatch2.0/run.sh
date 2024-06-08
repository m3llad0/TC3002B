#!/bin/bash

# Navigate to the backend directory and start the Flask backend server
echo "Starting Flask backend server..."
cd backend
pip install -r requirements.txt
export FLASK_APP=app.py  # Adjust this to the name of your Flask app file if different
flask run &
BACKEND_PID=$!

# Navigate to the frontend directory and start the Next.js frontend server
echo "Starting Next.js frontend server..."
cd ../frontend
npm install
npm run dev &
FRONTEND_PID=$!

# Function to kill the background processes when the script is terminated
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Trap script termination (Ctrl+C) and call the cleanup function
trap cleanup SIGINT SIGTERM

# Wait for the frontend and backend processes to end
wait $BACKEND_PID
wait $FRONTEND_PID
