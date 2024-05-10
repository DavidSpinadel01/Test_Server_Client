#!/bin/bash

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run server and clients
gnome-terminal -- python3 server.py
gnome-terminal -- python3 client.py
gnome-terminal -- python3 ai_client.py

pytest
