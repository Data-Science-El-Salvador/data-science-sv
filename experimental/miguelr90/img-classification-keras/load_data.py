import os
import argparse
import logging

from pathlib import Path

import numpy as np
from tensorflow import keras


def download():
    # download train/test splits
    logging.info("Downloading train/test split: using keras.datasets")
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    targets = [
        "T-shirt/top",
        "Trouser",
        "Pullover",
        "Dress",
        "Coat",
        "Sandal",
        "Shirt",
        "Sneaker",
        "Bag",
        "Ankle boot",
    ]

    # root path (IMPORTANT: don't move script from root path)
    root = Path(os.path.dirname(__file__))

    # data dir (make if not exists)
    data_dir = root.joinpath("data")
    data_dir.mkdir(exist_ok=True)
    logging.info("Data directory: %s", data_dir)

    # filenames to use
    names = [
        "train_images.npy",
        "train_labels.npy",
        "test_images.npy",
        "test_labels.npy",
        "targets.npy",
    ]

    # arrays to write
    arrays = [train_images, train_labels, test_images, test_labels, targets]

    for name, array in zip(names, arrays):

        path = data_dir.joinpath(name)

        if not path.exists():
            logging.info("Writing array to disk: %s" % name)
            np.save(path, array)
        else:
            logging.info("Skipping download: %s already exists!" % name)


def main():
    # parsing cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log", type=str, default="INFO", help="logging level: DEBUG, INFO, WARNING"
    )
    args = parser.parse_args()

    # logging setup for script
    numeric_level = getattr(logging, args.log.upper())
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % args.log)
    logging.basicConfig(level=numeric_level)

    # download and save data
    download()


if __name__ == "__main__":
    main()
