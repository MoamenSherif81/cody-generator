# Create bin directory and train the model
mkdir -p Extra/bin
python3 Model/train_our_model.py ./Extra/training_features ./Extra/validation_features ./Extra/bin 1

# Zip the bin directory
zip -r Extra/bin.zip Extra/bin/
