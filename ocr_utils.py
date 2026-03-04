import pytesseract
import cv2
import re
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def safe_extract(pattern, text, group_index=1):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            return match.group(group_index)
        except:
            return "Not Detected"
    return "Not Detected"

def run_ocr(image_path):

    try:
        image = cv2.imread(image_path)
        if image is None:
            return default_output()

        # Resize
        image = cv2.resize(image, None, fx=1.5, fy=1.5)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Light noise reduction
        gray = cv2.bilateralFilter(gray, 9, 75, 75)

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(gray, config=custom_config)

        # Extract only structured data
        return {
            "price": safe_extract(r"(₹\s?\d+|Rs\.?\s?\d+)", text),
            "expiry": safe_extract(r"\d{2}/\d{2}/\d{4}", text),
            "mfg_date": safe_extract(r"(MFG|Manufactured).*?(\d{2}/\d{2}/\d{4})", text, 2),
            "calories": safe_extract(r"(Energy|Calories)\D+(\d+\.?\d*)", text, 2),
            "protein": safe_extract(r"Protein\D+(\d+\.?\d*)", text),
            "fat": safe_extract(r"Fat\D+(\d+\.?\d*)", text),
            "carbs": safe_extract(r"(Carb|Carbohydrate)\D+(\d+\.?\d*)", text, 2),
            "fiber": safe_extract(r"Fiber\D+(\d+\.?\d*)", text),
            "sugar": safe_extract(r"Sugar\D+(\d+\.?\d*)", text),
        }

    except:
        return default_output()

def default_output():
    return {
        "price": "Not Detected",
        "expiry": "Not Detected",
        "mfg_date": "Not Detected",
        "calories": "Not Detected",
        "protein": "Not Detected",
        "fat": "Not Detected",
        "carbs": "Not Detected",
        "fiber": "Not Detected",
        "sugar": "Not Detected"
    }