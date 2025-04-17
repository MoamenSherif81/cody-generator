#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <number_of_samples> <path_to_pretrained_weights>"
  exit 1
fi

NUM_SAMPLES=$1
WEIGHTS_PATH=$2

mkdir -p Extra

# Navigate to Dataset directory
cd Dataset || exit

# Compile the C++ generator
g++ -std=c++17 -Iinclude basic_generator.cpp -o basic_generator

# Go back to root directory
cd ..

# Run generator
python3 Dataset/generator.py 281203 "$NUM_SAMPLES" ./Extra

# Install Playwright and dependencies
pip install playwright
playwright install

# Render HTML to GUI
cd Compiler || exit
python3 Renderer.py ../Extra/input ../Extra/input
cd ..

# Split the data
python3 Model/build_datasets.py Extra/input

# Convert input to features
mkdir -p Extra/training_features
python3 Model/convert_to_features.py ./Extra/training ./Extra/training_features

mkdir -p Extra/validation_features
python3 Model/convert_to_features.py ./Extra/validation ./Extra/validation_features

# Create bin directory for output model
mkdir -p Extra/bin

# Train with pretrained weights
python3 Model/train.py ./Extra/training_features ./Extra/validation_features ./Extra/bin 1 "$WEIGHTS_PATH"

# Zip the final trained weights
zip -r Extra/bin.zip Extra/bin/
