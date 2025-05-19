from keras.api.layers import (
    Input,
    Dense,
    Dropout,
    RepeatVector,
    LSTM,
    concatenate,
    Conv2D,
    Flatten,
    MaxPooling2D,
)
from keras.api.models import Sequential, Model
from keras.api.optimizers import RMSprop

from .AModel import AModel
from .config import CONTEXT_LENGTH, EPOCHS, BATCH_SIZE


class pix2code_model(AModel):
    def __init__(self, input_shape, output_size, output_path):
        AModel.__init__(self, input_shape, output_size, output_path)
        self.name = "pix2code_model"

        image_model = Sequential()
        image_model.add(Input(input_shape))
        image_model.add(Conv2D(32, (3, 3), padding="valid", activation="relu"))
        image_model.add(Conv2D(32, (3, 3), padding="valid", activation="relu"))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))
        image_model.add(Dropout(0.25))

        image_model.add(Conv2D(64, (3, 3), padding="valid", activation="relu"))
        image_model.add(Conv2D(64, (3, 3), padding="valid", activation="relu"))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))
        image_model.add(Dropout(0.25))

        image_model.add(Conv2D(128, (3, 3), padding="valid", activation="relu"))
        image_model.add(Conv2D(128, (3, 3), padding="valid", activation="relu"))
        image_model.add(MaxPooling2D(pool_size=(2, 2)))
        image_model.add(Dropout(0.25))

        image_model.add(Flatten())
        image_model.add(Dense(1024, activation="relu"))
        image_model.add(Dropout(0.3))
        image_model.add(Dense(1024, activation="relu"))
        image_model.add(Dropout(0.3))

        image_model.add(RepeatVector(CONTEXT_LENGTH))

        visual_input = Input(shape=input_shape)
        encoded_image = image_model(visual_input)

        language_model = Sequential()
        language_model.add(
            LSTM(128, return_sequences=True, input_shape=(CONTEXT_LENGTH, output_size))
        )
        language_model.add(LSTM(128, return_sequences=True))

        textual_input = Input(shape=(CONTEXT_LENGTH, output_size))
        encoded_text = language_model(textual_input)

        decoder = concatenate([encoded_image, encoded_text])

        decoder = LSTM(512, return_sequences=True)(decoder)
        decoder = LSTM(512, return_sequences=False)(decoder)
        decoder = Dense(output_size, activation="softmax")(decoder)

        self.model = Model(inputs=[visual_input, textual_input], outputs=decoder)

        optimizer = RMSprop(learning_rate=0.0001, clipvalue=1.0)
        self.model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

    def fit(self, images, partial_captions, next_words, validation_data=None):
        self.model.fit(
            [images, partial_captions],
            next_words,
            shuffle=False,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            verbose=1,
            validation_data=validation_data,  # expects a tuple: ([val_images, val_captions], val_next_words)
        )
        self.save()

    def fit_generator(
            self,
            train_generator,
            steps_per_epoch,
            validation_generator=None,
            validation_steps=None,
    ):
        self.model.fit(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            validation_data=validation_generator,
            validation_steps=validation_steps,
            epochs=EPOCHS,
            verbose=1,
        )
        self.save()

    def predict(self, image, partial_caption):
        return self.model.predict([image, partial_caption], verbose=0)[0]

    def predict_batch(self, images, partial_captions):
        return self.model.predict([images, partial_captions], verbose=1)
