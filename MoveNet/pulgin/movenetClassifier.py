import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split

from .script.data import BodyPart


def get_center_point(landmarks, left_bodypart, right_bodypart):
    left = tf.gather(landmarks, left_bodypart.value, axis=1)
    right = tf.gather(landmarks, right_bodypart.value, axis=1)
    return left * 0.5 + right * 0.5


def get_pose_size(landmarks, torso_size_multiplier=2.5):
    hips_center = get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP)
    shoulders_center = get_center_point(landmarks, BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER)
    torso_size = tf.linalg.norm(shoulders_center - hips_center)
    pose_center_new = tf.expand_dims(get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP), axis=1)
    pose_center_new = tf.broadcast_to(pose_center_new, [tf.size(landmarks) // (17 * 2), 17, 2])
    d = tf.gather(landmarks - pose_center_new, 0, axis=0, name="dist_to_pose_center")
    return tf.maximum(torso_size * torso_size_multiplier, tf.reduce_max(tf.linalg.norm(d, axis=0)))


def normalize_pose_landmarks(landmarks):
    pose_center = tf.expand_dims(get_center_point(landmarks, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP), axis=1)
    pose_center = tf.broadcast_to(pose_center, [tf.size(landmarks) // (17 * 2), 17, 2])
    landmarks = landmarks - pose_center
    return landmarks / get_pose_size(landmarks)


def landmarks_to_embedding(landmarks_and_scores):
    reshaped_inputs = keras.layers.Reshape((17, 3))(landmarks_and_scores)
    return keras.layers.Flatten()(normalize_pose_landmarks(reshaped_inputs[:, :, :2]))


class MoveNetClassifier(object):
    def __init__(self):
        self.model = None

    def build_model(self, class_names=None, model_path=None):
        if model_path:
            self.model = keras.models.load_model(model_path)
        else:
            inputs = keras.Input(shape=(51))
            embedding = landmarks_to_embedding(inputs)

            layer = keras.layers.Dense(128, activation=tf.nn.relu6)(embedding)
            layer = keras.layers.Dropout(0.5)(layer)
            layer = keras.layers.Dense(64, activation=tf.nn.relu6)(layer)
            layer = keras.layers.Dropout(0.5)(layer)
            outputs = keras.layers.Dense(len(class_names), activation="softmax")(layer)

            self.model = keras.Model(inputs, outputs)
            self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def train(self, X_data, y_data, test_size=0.15, monitor="val_accuracy", patience=20,
              batch_size=16, epochs=200, cp_path="best.weight.hdf5", save_path=None):
        X_train, X_val, y_train, y_val = train_test_split(X_data, y_data, test_size=test_size)
        checkpoint = keras.callbacks.ModelCheckpoint(cp_path, monitor=monitor, verbose=1, save_best_only=True,
                                                     mode='max')
        early_stopping = keras.callbacks.EarlyStopping(monitor=monitor, patience=patience)
        his = self.model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs,
                             callbacks=[checkpoint, early_stopping], validation_data=(X_val, y_val))
        if save_path:
            self.model.save(save_path)
        return his

    def evaluate(self, X, y):
        return self.model.evaluate(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save_model(self, save_path, save_name="pose_classifier"):
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        model = converter.convert()

        with open(f'{save_path}/{save_name}.tflite', 'wb') as f:
            f.write(model)
        print('Model size: %dKB' % (len(model) / 1024))
