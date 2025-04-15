#!/bin/bash

# Check if an argument was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <number_of_samples>"
  exit 1
fi

NUM_SAMPLES=$1

mkdir -p Extra

# Navigate to Dataset directory
cd Dataset || exit

# Compile the C++ generator
g++ -std=c++17 -Iinclude basic_generator.cpp -o basic_generator

# Go back to root directory
cd ..

# Run generator.py with the input number
python3 Dataset/generator.py 281203 "$NUM_SAMPLES" ./Extra

# Install Playwright and its dependencies
pip install playwright
playwright install

# Navigate to Compiler directory and run Renderer
cd Compiler || exit
python3 Renderer.py ../Extra/input ../Extra/input

# Go back to root directory
cd ..

# Create input_features directory and convert input to features
mkdir -p Extra/input_features
python3 Model/convert_to_features.py ./Extra/input ./Extra/input_features

# Create bin directory and train the model
mkdir -p Extra/bin
python3 Model/train.py ./Extra/input_features ./Extra/bin 1

# Zip the bin directory
zip -r Extra/bin.zip Extra/bin/
