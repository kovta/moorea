#!/bin/bash
set -e

echo "Installing build dependencies first..."
pip install --upgrade setuptools wheel setuptools_scm

echo "Installing PyTorch (CPU version)..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo "Installing remaining dependencies with --no-build-isolation..."
pip install --no-build-isolation -r backend/requirements.txt

echo "Build complete!"
