import os
import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt

from prediction.yolov5.utils.general import non_max_suppression, scale_segments
# from prediction.yolov5.utils.dataloaders import LoadImages
import urllib.request
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
root_dir =BASE_DIR / 'prediction/yolov5'
os.chdir(root_dir)

from .yolov5.models.experimental import attempt_load

model = attempt_load(f"{BASE_DIR}\prediction\yolov5\\best.pt")


# Load an image
def load_img(url):
    img_path = url
    with urllib.request.urlopen(img_path) as resp:
        # read image as an numpy array
        img = np.asarray(bytearray(resp.read()), dtype="uint8")

        # use imdecode function
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        # display image
    # img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 640))
    return img


def tree_count(url):
    # load the image
    img = load_img(url)
    # convert from numpy to tensor
    img2 = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
    img2 = img2.unsqueeze(0)  # Add batch dimension

    # tree detection
    pred = model(img2)[0]

    # Apply non-maximum suppression (NMS) to get the most confident detections
    pred = non_max_suppression(pred, 0.5, 0.4)

    target_class = "tree"

    # Initialize a counter for the desired class
    class_count = 0
    # Iterate through the detection results
    for det in pred[0]:
        print("iteration",class_count)
        class_count += 1
        x1, y1, x2, y2 = map(int, det[:4])

        # img=img.squeeze(0)
        # img=img.numpy()

        # Draw the bounding box and label on the image
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Green rectangle

        # Add a label near the bounding box
        label = f"{target_class} ({det[4]:.2f})"
        cv2.putText(
            img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
        )

        # save the produced images
        directory = f"{BASE_DIR}\predictedImages"
        file_name = url.split("/")[4]
        os.chdir(directory)
        cv2.imwrite(file_name, img)
    return class_count
