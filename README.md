# AI-Based Grocery Item Recognition & Intelligence System

This project presents an AI-powered grocery item recognition system developed during an AI/ML internship. The system uses deep learning, computer vision, OCR, and a Streamlit dashboard to identify grocery products from images and display detailed information such as nutritional values, shelf life, and health insights.

The goal of this project is to assist small retail stores and grocery shops by providing an intelligent offline system that can automatically recognize grocery items and provide useful product information.

---

## Project Overview

Traditional grocery stores often deal with loose items and unlabelled products that cannot be scanned through barcodes. This project solves that problem by using image classification and OCR techniques to automatically identify grocery items.

The system works completely offline and provides the following functionalities:

* Image based grocery item recognition
* Nutritional information retrieval
* Shelf life and storage suggestions
* Health score analysis
* OCR based price and expiry detection for packaged products
* Interactive Streamlit dashboard interface

---

## Technologies Used

* Python
* PyTorch
* EfficientNet-B0 (Deep Learning Model)
* Tesseract OCR
* SQLite Database
* Streamlit Dashboard
* OpenCV
* Scikit-learn

---

## System Architecture

The system follows a multi-stage pipeline:

1. User uploads or captures a grocery item image
2. Image preprocessing is applied (resize, normalization)
3. EfficientNet-B0 model performs image classification
4. Predicted label is used to query the SQLite database
5. OCR module extracts text from packaged products
6. Results are displayed in the Streamlit dashboard

The dashboard presents the item name, confidence score, nutrition information, health score, price, expiry date, and alternative suggestions.

---

## Dataset

Due to file size limitations, the dataset is not stored directly in this repository.

The dataset used for training and evaluation can be downloaded from the following link:

Dataset Link: https://drive.google.com/

### Dataset Details

Total Images: 5643
Total Classes: 60 grocery categories

### Dataset Structure

Grocery_Dataset/

train/
validation/
test/

Each folder contains categorized grocery item images used for training, validation, and testing of the deep learning model.

---

## Model Information

The system uses the EfficientNet-B0 convolutional neural network architecture for image classification.

Transfer learning was applied using pretrained ImageNet weights and the final classification layer was modified to support the grocery dataset classes.

Training configuration:

Batch Size: 32
Optimizer: Adam
Learning Rate: 5e-4
Loss Function: Cross Entropy Loss
Epochs: 15

Final Test Accuracy: ~88%

---

## OCR Module

For packaged products, the system uses Tesseract OCR to extract textual information from the product image.

The OCR module detects:

* Product price
* Expiry date
* Printed label text

The extracted information is combined with the classification results and displayed in the dashboard.

---

## Database Design

A local SQLite database is used to store product information.

The database includes:

* Product category
* Item name
* Local name
* Nutritional information
* Shelf life
* Storage advice
* Health score
* Alternative product suggestions

This allows the system to provide useful information along with the item prediction.

---

## Streamlit Dashboard

A Streamlit-based user interface was developed to allow users to interact wit

