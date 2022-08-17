#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology

"""Extract images from a rosbag.
"""

import argparse
import os
import pdb

import cv2
import rosbag
from cv_bridge import CvBridge
import numpy as np
from glob import glob


def parse_args():
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_files", help="Input ROS bag or quoted wildcard pattern.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("image_topic", help="Image topic.")
    parser.add_argument(
        "--start-index",
        help="Which file to start from if using a wildcard pattern",
        default=0,
        type=int,
    )
    parser.add_argument(
        "--end-index", help="Which file to end on if using a wildcard pattern", type=int
    )
    parser.add_argument(
        "--delta", type=float, help="time between consequetive images", default=0.1
    )
    parser.add_argument(
        "--flip-channels",
        action="store_true",
        help="Flip from RGB to BRG or vice versa",
    )
    parser.add_argument(
        "--debayer",
        action="store_true",
        help="Assume that input is stored as a Bayered image",
    )

    args = parser.parse_args()
    return args


def save_images_from_bag(
    bag_file, image_topic, output_dir, flip, delta=0.1, debayer=False, last_time=0
):
    bag = rosbag.Bag(bag_file, "r")
    bridge = CvBridge()
    for _, msg, t in bag.read_messages(topics=[image_topic]):
        if (t.to_time() - last_time) < delta:
            continue

        img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        if debayer:
            img = cv2.cvtColor(img, cv2.COLOR_BayerBG2RGB)

        if flip:
            img = np.flip(img, axis=2)
        cv2.imwrite(os.path.join(output_dir, "time_%07f.png" % t.to_time()), img)
        last_time = t.to_time()

    bag.close()
    return last_time


def main():
    """Extract a folder of images from a rosbag.
    """
    args = parse_args()

    print(
        "Extract images from %s on topic %s into %s"
        % (args.bag_files, args.image_topic, args.output_dir)
    )
    files = sorted(glob(args.bag_files))

    output_dir = os.path.join(
        args.output_dir, args.image_topic[1:-10].replace("/", "_")
    )

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    last_time = 0
    for file in files[args.start_index : args.end_index]:
        print("processing {}".format(file))
        last_time = save_images_from_bag(
            file,
            args.image_topic,
            output_dir,
            args.flip_channels,
            args.delta,
            debayer=args.debayer,
            last_time=last_time,
        )


if __name__ == "__main__":
    main()
