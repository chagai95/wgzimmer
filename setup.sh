#!/bin/bash

# WGZimmer Ad Booster - Setup Script

echo "====================================="
echo "WGZimmer Ad Booster Setup"
echo "====================================="

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --break-system-packages -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Make the main script executable
chmod +x wgzimmer_boost.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  - Test run (visible browser): python3 wgzimmer_boost.py --once"
echo "  - Continuous mode: python3 wgzimmer_boost.py"
echo ""
echo "To run in background:"
echo "  nohup python3 wgzimmer_boost.py > output.log 2>&1 &"
echo ""
