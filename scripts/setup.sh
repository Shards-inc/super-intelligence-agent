#!/bin/bash
# Enterprise Setup Script
set -e

echo "Initializing Enterprise AI Agent Environment..."

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please update it with your API keys."
fi

echo "Setup complete."
