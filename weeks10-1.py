from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.datasets import cifar10
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import os
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# for i in range(10):
#     plt.imshow(train_images[i])
#     plt.xlabel(class_names[train_labels[i][0]])
#     plt.show()

train_images = train_images.reshape(train_images.shape[0], train_images.shape[1], train_images.shape[2], 3).astype('float32') / 255
test_images = test_images.reshape(test_images.shape[0], test_images.shape[1], test_images.shape[2], 3).astype('float32') / 255
train_labels = np_utils.to_categorical(train_labels)
test_labels = np_utils.to_categorical(test_labels)

model = Sequential()
model.add(Conv2D(32, kernel_size = (3, 3), input_shape=(32, 32, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
             metrics=['accuracy'])

print('model compile')

MODEL_DIR = './model/'
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

modelpath = './model/lab16-{epoch:02d}.hdf5'
checkpointer = ModelCheckpoint(filepath=modelpath, monitor='val_loss', verbose=1, save_best_only=True)
early_stopping = EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=30, batch_size=200, verbose=0, callbacks=[checkpointer, early_stopping])

test_eval = model.evaluate(test_images, test_labels)
print("Test Accuracy : %.4f" % test_eval)
test_predict = model.predict(test_images)

for i in range(10):
    print("Actual class: %d => Expect Class: %d" % (test_labels[i], test_predict[i]))

    

