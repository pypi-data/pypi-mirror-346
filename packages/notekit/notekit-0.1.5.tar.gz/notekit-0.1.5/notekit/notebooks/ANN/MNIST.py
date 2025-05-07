# !pip install tensorflow

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, losses
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# Step 1: Load and preprocess MNIST data
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize (just like PyTorch ToTensor + Normalize(0.5,0.5))
x_train = (x_train / 255.0 - 0.5) / 0.5
x_test = (x_test / 255.0 - 0.5) / 0.5

# Labels don't need to be one-hot because sparse_categorical_crossentropy accepts integer labels

# Step 2: Define the model
model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(10)  # logits output (we'll apply softmax in loss)
])

# Step 3: Compile the model
model.compile(
    optimizer=optimizers.Adam(learning_rate=0.001),
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

# Step 4: Train the model
model.fit(x_train, y_train, epochs=5, batch_size=64)

# Step 5: Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f'Accuracy: {test_acc * 100:.2f}%')
