import os
import sys
import argparse
import logging

from pathlib import Path

import numpy as np
from tensorflow import keras


def load_data():
    # root path (IMPORTANT: don't move script from root path)
    root = Path(os.path.dirname(__file__))

    # data dir (make if not exists)
    data_dir = root.joinpath("data")

    if not data_dir.exists():
        logging.error("No train data available: run load_data.py first!")
        raise FileNotFoundError

    names = [
        "train_images.npy",
        "train_labels.npy",
        "test_images.npy",
        "test_labels.npy",
        "targets.npy",
    ]

    variables = ["x_train", "y_train", "x_test", "y_test", "tragets"]

    # storage dict
    data = {}

    # load files
    for name, var in zip(names, variables):
        try:
            data[var] = np.load(data_dir.joinpath(name))
        except FileNotFoundError:
            logging.error("Cannot load %s: re-run load_data.py" % name)
            sys.exit()

    return data


def train(epochs=10, validate=True):

    data = load_data()

    model = keras.Sequential(
        [
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(10, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    model.fit(data["x_train"], data["y_train"], epochs=epochs)

    if validate:
        test_loss, test_acc = model.evaluate(data["x_test"], data["y_test"], verbose=2)
        logging.info("Test accuracy: %s" % test_acc)


def main():
    # parsing cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--epochs", type=int, default=10, help="num of epochs to run traning"
    )
    parser.add_argument(
        "--log", type=str, default="INFO", help="logging level: DEBUG, INFO, WARNING"
    )
    args = parser.parse_args()

    # logging setup for script
    numeric_level = getattr(logging, args.log.upper())
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % args.log)
    logging.basicConfig(level=numeric_level)

    # train model
    train(epochs=args.epochs)


if __name__ == "__main__":
    main()
