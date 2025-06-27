import tensorflow as tf
from keras.api import layers, Model
from keras.api.applications import ResNet50
import numpy as np
from classes.models.config import CONTEXT_LENGTH, NUM_DECODER_LAYERS, D_MODEL, NHEAD, DIM_FORWARD, FREEZE_CNN, BATCH_SIZE, EPOCHS

class ResnetTransformerModel:
    def __init__(self, input_shape, output_size, output_path, dropout_rate=0.1):
        self.input_shape = input_shape
        self.output_size = output_size
        self.output_path = output_path
        self.model = None
        self.dropout_rate = dropout_rate
        
        # Model hyperparameters
        self.transformer_layers = NUM_DECODER_LAYERS
        self.d_model = D_MODEL
        self.num_heads = NHEAD
        self.dff = DIM_FORWARD  # Feed forward network dimension
        
        self.build()
        
    def build_cnn_encoder(self):
        """Build the CNN encoder using a pre-trained ResNet model with frozen weights"""
        # Load ResNet with pre-trained weights, without the classification head
        base_model = ResNet50(
            include_top=False, 
            weights='imagenet', 
            input_shape=self.input_shape,
            pooling='avg'
        )
        
        # Freeze the ResNet weights
        for layer in base_model.layers:
            layer.trainable = not FREEZE_CNN
            
        # Get the output of the ResNet model
        cnn_features = base_model.output
        
        # Add an adapter layer to project CNN features to transformer dimensions
        adapter = layers.Dense(self.d_model, name="cnn_adapter")(cnn_features)
        adapter = layers.LayerNormalization(epsilon=1e-6)(adapter)
        
        return base_model.input, adapter
    
    def build_transformer_decoder(self, cnn_features):
        """Build the transformer decoder"""
        # Input for tokenized partial sequences
        seq_input = layers.Input(shape=(CONTEXT_LENGTH, self.output_size))
        
        # Project binary vectors to embedding space
        seq_embedding = layers.Dense(self.d_model)(seq_input)
        
        # Add positional encoding
        pos_encoding = self.positional_encoding(CONTEXT_LENGTH, self.d_model)
        # CHANGED: Use layers.Add() and Lambda instead of direct addition
        seq_embedding = layers.Add()([seq_embedding, layers.Lambda(lambda x: pos_encoding)(seq_embedding)])
        
        # Dropout for regularization
        decoder_input = layers.Dropout(self.dropout_rate)(seq_embedding)
        
        # Create a batch of identical CNN features to match sequence length
        cnn_context = layers.Dense(self.d_model)(cnn_features)
        
        # CHANGED: Instead of using tf.expand_dims and tf.repeat, use Keras layers
        # First reshape to add a time dimension
        cnn_context = layers.Reshape((1, self.d_model))(cnn_context)
        
        # Then repeat the features across the time dimension using Lambda
        cnn_context = layers.Lambda(
            lambda x: tf.repeat(x, repeats=CONTEXT_LENGTH, axis=1),
            name="repeat_cnn_features"
        )(cnn_context)
        
        # Stack transformer decoder layers
        decoder_output = decoder_input
        for i in range(self.transformer_layers):
            decoder_output = self.transformer_decoder_layer(
                decoder_output, 
                cnn_context,
                f"decoder_layer_{i}"
            )
        
        # Final output projection
        final_output = layers.Dense(self.output_size, activation='softmax')(decoder_output)
        
        # CHANGED: We only care about the prediction for the last token in the sequence
        last_token_output = layers.Lambda(lambda x: x[:, -1, :])(final_output)
        
        return seq_input, last_token_output
    
    def transformer_decoder_layer(self, inputs, context, name_prefix):
        """Single transformer decoder layer with self-attention and cross-attention"""
        # Self attention (masked)
        self_attn_output = self.multi_head_attention(
            inputs, inputs, inputs, 
            name=f"{name_prefix}_self_attn"
        )
        self_attn_output = layers.Dropout(self.dropout_rate)(self_attn_output)
        # CHANGED: Use layers.Add() instead of direct addition
        self_attn_output = layers.LayerNormalization(epsilon=1e-6)(layers.Add()([inputs, self_attn_output]))
        
        # Cross attention with CNN features
        cross_attn_output = self.multi_head_attention(
            self_attn_output, context, context,
            name=f"{name_prefix}_cross_attn"
        )
        cross_attn_output = layers.Dropout(self.dropout_rate)(cross_attn_output)
        # CHANGED: Use layers.Add() instead of direct addition
        cross_attn_output = layers.LayerNormalization(epsilon=1e-6)(layers.Add()([self_attn_output, cross_attn_output]))
        
        # Feed forward network
        ffn_output = self.feed_forward_network(cross_attn_output, name=f"{name_prefix}_ffn")
        ffn_output = layers.Dropout(self.dropout_rate)(ffn_output)
        # CHANGED: Use layers.Add() instead of direct addition
        output = layers.LayerNormalization(epsilon=1e-6)(layers.Add()([cross_attn_output, ffn_output]))
        
        return output
    
    def multi_head_attention(self, q, k, v, name):
        """Multi-head attention layer"""
        attention = layers.MultiHeadAttention(
            num_heads=self.num_heads,
            key_dim=self.d_model // self.num_heads,
            name=name
        )
        return attention(q, k, v)
    
    def feed_forward_network(self, inputs, name):
        """Feed forward network for transformer"""
        x = layers.Dense(self.dff, activation='relu', name=f"{name}_dense1")(inputs)
        x = layers.Dense(self.d_model, name=f"{name}_dense2")(x)
        return x
    
    def positional_encoding(self, max_seq_len, d_model):
        """Create positional encodings for the transformer"""
        position = np.expand_dims(np.arange(0, max_seq_len), axis=1)
        div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))
        
        pos_encoding = np.zeros((1, max_seq_len, d_model))
        pos_encoding[0, :, 0::2] = np.sin(position * div_term)
        pos_encoding[0, :, 1::2] = np.cos(position * div_term)
        
        return tf.cast(pos_encoding, dtype=tf.float32)
    
    def build(self):
        """Build the complete model architecture"""
        # Build CNN Encoder
        img_input, cnn_features = self.build_cnn_encoder()
        
        # Build Transformer Decoder
        seq_input, output = self.build_transformer_decoder(cnn_features)
        
        # Create the model with both inputs
        self.model = Model(inputs=[img_input, seq_input], outputs=output)
        
        # Compile the model
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(self.model.summary())
    
    def fit(self, images, partial_sequences, next_words, validation_data):
        """Train the model with the provided data"""
        callbacks = self.get_callbacks()
        
        self.model.fit(
            [images, partial_sequences], next_words,
            validation_data=validation_data,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            callbacks=callbacks
        )
    
    def fit_generator(self, generator, steps_per_epoch, validation_generator=None, validation_steps=None):
        """Train the model using a generator"""
        callbacks = self.get_callbacks()
        
        self.model.fit(
            generator,
            steps_per_epoch=steps_per_epoch,
            validation_data=validation_generator,
            validation_steps=validation_steps,
            epochs=EPOCHS,
            callbacks=callbacks
        )
    
    def get_callbacks(self):
        """Define callbacks for the training process"""
        checkpoint_path = f"{self.output_path}/checkpoint.h5"
        checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path,
            monitor='val_accuracy',
            verbose=1,
            save_best_only=True,
            save_weights_only=True
        )
        
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )
        
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            min_lr=1e-6
        )
        
        return [checkpoint_callback, early_stopping, reduce_lr]
    
    def predict(self, image, partial_sequence):
        """Generate a prediction for the next token"""
        return self.model.predict([image, partial_sequence])
    
    def save(self):
        """Save the model weights"""
        self.model.save_weights(f"{self.output_path}/model_weights.h5")
    
    def load(self, weights_path):
        """Load the model weights"""
        self.model.load_weights(weights_path)