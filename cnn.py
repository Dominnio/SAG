# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

import numpy as np
from keras.preprocessing import image

#for testing
import agent_config

class CNN:
    num_of_instances = 0

    def __init__(self, dir):  # konstruktor
        self.training_set_path = str(dir['training_set_path'])
        self.test_set_path = str(dir['test_set_path'])
        self.spe = int(dir['steps_per_epoch'])
        self.no_epochs = int(dir['epochs'])
        self.vs = int(dir['validation_steps'])

        self.cnn_classificator_training(self.training_set_path, self.test_set_path, self.spe,
                                        self.no_epochs, self.vs)
        CNN.num_of_instances += 1

    # Note - be careful with dataset classes directory order - main class directory ( for example folder cat) should always be above other directory ( above other_than_cat)

    def cnn_classificator_training(self, training_set_path, test_set_path, spe, no_epochs, vs):

        self.classifier = Sequential()  # Initialising the CNN

        self.classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))  # Step 1 - Convolution
        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))  # Step 2 - Pooling

        self.classifier.add(Conv2D(32, (3, 3), activation='relu'))  # Adding a second convolutional layer
        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))

        self.classifier.add(Flatten())  # Step 3 - Flattening

        self.classifier.add(Dense(units=128, activation='relu'))  # Step 4 - Full connection
        self.classifier.add(Dense(units=1, activation='sigmoid'))

        self.classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])  # Compiling the CNN

        from keras.preprocessing.image import ImageDataGenerator  # Part 2 - Fitting the CNN to the images
        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True)
        test_datagen = ImageDataGenerator(rescale=1. / 255)

        self.training_set = train_datagen.flow_from_directory(training_set_path,
                                                              target_size=(64, 64),
                                                              batch_size=32,
                                                              class_mode='binary')
        test_set = test_datagen.flow_from_directory(test_set_path,
                                                    target_size=(64, 64),
                                                    batch_size=32,
                                                    class_mode='binary')
        self.classifier.fit_generator(self.training_set,
                                      steps_per_epoch=spe,
                                      epochs=no_epochs,
                                      validation_data=test_set,
                                      validation_steps=vs)

    def predict(self, img_path):

        # Part 3 - Making new predictions
        self.test_image = image.load_img(img_path, target_size=(64, 64))
        self.test_image = image.img_to_array(self.test_image)
        self.test_image = np.expand_dims(self.test_image, axis=0)
        self.result = self.classifier.predict(self.test_image)
        self.training_set.class_indices
        if self.result[0][0] == 1:
            return 0
        else:
            return 1

# ## For testing
# agent = CNN(agent_config.agent_4)
#
# is_animal = [agent.predict(str(agent_config.test_images['cat1'])),
#           agent.predict(str(agent_config.test_images['cat2'])),
#           agent.predict(str(agent_config.test_images['dog1'])),
#           agent.predict(str(agent_config.test_images['dog2'])),
#           agent.predict(str(agent_config.test_images['chicken1'])),
#           agent.predict(str(agent_config.test_images['chicken2'])),
#           agent.predict(str(agent_config.test_images['horse1'])),
#           agent.predict(str(agent_config.test_images['horse2']))]
#
# for x in is_animal:
#     if is_animal[x] == 1:
#         print('chicken')
#     else:
#         print('not chicken')

