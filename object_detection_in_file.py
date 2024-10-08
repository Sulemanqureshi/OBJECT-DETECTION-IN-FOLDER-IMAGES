# -*- coding: utf-8 -*-
"""Object Detection in File.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gl1LN8i9dqg1rJzyMBIoZHCApbTOpcn0
"""

!pip install ultralytics

import cv2
import os
import zipfile
from google.colab import files
from ultralytics import YOLO
from IPython.display import display, Image
import numpy as np

def process_images(input_folder, output_folder, model, conf_threshold=0.25):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            print(f"Processing image: {image_path}")

            # Read image
            img = cv2.imread(image_path)
            if img is None:
                print(f"Error reading image: {image_path}")
                continue

            # Perform detection
            results = model(img)
            result = results[0]

            detections = []
            for box in result.boxes:
                conf = float(box.conf)
                if conf >= conf_threshold:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls)
                    label = f"{result.names[cls]} {conf:.2f}"

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    detections.append((result.names[cls], conf))

            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)

            print(f"Processed {filename}:")
            if detections:
                for obj, conf in detections:
                    print(f"  - with confidence {conf:.2f}")
            else:
                print("  - No objects detected")

# Upload a ZIP file containing a folder of images
uploaded = files.upload()
zip_path = next(iter(uploaded))

# Extract the ZIP file
extracted_folder = 'images'
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)
    print(f"Extracted ZIP file to: {extracted_folder}")

# Find the first subfolder in the extracted folder
subfolders = [f for f in os.listdir(extracted_folder) if os.path.isdir(os.path.join(extracted_folder, f))]
if not subfolders:
    print("No subfolders found in the extracted ZIP file.")
    exit()

input_folder = os.path.join(extracted_folder, subfolders[0])
print(f"Using input folder: {input_folder}")

# List files in the input folder
input_files = os.listdir(input_folder)
print(f"Files in input folder: {input_files}")

output_folder = 'detected_images'

# Load the YOLO model
model = YOLO('yolov8n.pt')  # Load the smallest YOLOv8 model

# Set a confidence threshold
CONFIDENCE_THRESHOLD = 0.4  # Adjust this value as needed

# Process images in the folder
process_images(input_folder, output_folder, model, conf_threshold=CONFIDENCE_THRESHOLD)

# Debug: List contents of the output folder
output_files = os.listdir(output_folder)
print(f"Files in output folder after processing: {output_files}")

# Display an example result
if output_files:
    example_image = os.path.join(output_folder, output_files[0])
    display(Image(example_image))
else:
    print("No images were processed. Please check the input folder and ensure it contains valid image files.")

# detected objects for each image
for filename in output_files:
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(output_folder, filename)
        results = model(image_path)
        result = results[0]
        print(f"\nDetections in {filename}:")
        for box in result.boxes:
            conf = float(box.conf)
            if conf >= CONFIDENCE_THRESHOLD:
                cls = int(box.cls)
                print(f"  - {result.names[cls]} (confidence: {conf:.2f})")