#!/bin/bash
# Script to restart the backend with our fixed dramatic bridal classification

echo "🧹 Killing any existing backend processes..."
pkill -f "uvicorn.*app.main"
sleep 2

echo "🚀 Starting backend with dramatic bridal boost..."
cd /Users/kovacstamaspal/dev/moorea/backend

# Start in background with screen
screen -dmS backend python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

sleep 5

echo "🏥 Checking backend health..."
curl -s http://localhost:8000/health

echo -e "\n✅ Backend restarted! Now test your bridal dress upload."
echo "Expected: bridal_ballgown or bridal_princess at 60%+ confidence (12% × 5 boost)"
