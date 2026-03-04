import os
import torch
import sqlite3
from torchvision import transforms, models
from PIL import Image
from ocr_utils import run_ocr

# ---------------- CONFIG ----------------

MODEL_PATH = r"C:/Users/91876/OneDrive/Documents/AI GROCERY RECOGNITION/AI-GROCERY-ITEM-RECOGNITION/models/grocery_model.pth"
TRAIN_DIR = r"C:/Users/91876/OneDrive/Documents/AI GROCERY RECOGNITION/AI-GROCERY-ITEM-RECOGNITION/Grocery Dataset/train data"
DB_PATH = r"C:/Users/91876/OneDrive/Documents/AI GROCERY RECOGNITION/AI-GROCERY-ITEM-RECOGNITION/database.db"

IMG_SIZE = 224
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- LOAD CLASSES ----------------

def get_classes(train_dir):
    classes = []
    for root, dirs, files in os.walk(train_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                relative_path = os.path.relpath(root, train_dir)
                label = relative_path.replace(os.sep, "_")
                classes.append(label)
    return sorted(list(set(classes)))

classes = get_classes(TRAIN_DIR)
num_classes = len(classes)

# ---------------- LOAD MODEL ----------------

model = models.efficientnet_b0(weights=None)
in_features = model.classifier[1].in_features
model.classifier[1] = torch.nn.Linear(in_features, num_classes)

model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()

transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor()
])

# ---------------- MAIN FUNCTION ----------------

def predict(image_path):

    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    confidence_value = confidence.item()
    confidence_percent = round(confidence_value * 100, 2)

    # UNKNOWN CONDITION
    if confidence_value < 0.5:
        return {
            "Item": "Unknown",
            "Confidence": confidence_percent
        }

    predicted_label = classes[predicted.item()]
    parts = predicted_label.split("_")

    # ---------------- PARSE LABEL ----------------

    packaging_raw = parts[0]              # Packaged / Unpackaged
    category = parts[1] if len(parts) > 1 else None
    item = parts[2] if len(parts) > 2 else None
    subtype = parts[3] if len(parts) > 3 else None
    brand = parts[4] if len(parts) > 4 else None

    packaging_type = "Loose" if packaging_raw.lower() == "unpackaged" else "Packaged"

    # ---------------- SQLITE FETCH ----------------

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if packaging_type == "Packaged":
        cursor.execute("""
            SELECT price_range, calories, protein, fat, carbs,
                   fiber, sugar, shelf_life,
                   storage_advice, health_score,
                   dietary_tag, alternative_item
            FROM grocery_items
            WHERE LOWER(item_name)=?
            AND LOWER(subtype)=?
            AND LOWER(brand)=?
            AND packaging_type=?
        """, (
            item.lower() if item else None,
            subtype.lower() if subtype else None,
            brand.lower() if brand else None,
            packaging_type
        ))
    else:
        cursor.execute("""
            SELECT price_range, calories, protein, fat, carbs,
                   fiber, sugar, shelf_life,
                   storage_advice, health_score,
                   dietary_tag, alternative_item
            FROM grocery_items
            WHERE LOWER(item_name)=?
            AND LOWER(subtype)=?
            AND packaging_type=?
        """, (
            item.lower() if item else None,
            subtype.lower() if subtype else None,
            packaging_type
        ))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "Item": item,
            "Subtype": subtype,
            "Brand": brand,
            "Packaging": packaging_type,
            "Confidence": confidence_percent,
            "Error": "Database match not found"
        }

    (db_price, db_cal, db_prot, db_fat, db_carbs,
     db_fiber, db_sugar, db_shelf,
     db_storage, db_health,
     db_diet, db_alternative) = row

    # ---------------- OCR (Only For Packaged) ----------------

    ocr_data = {}
    if packaging_type == "Packaged":
        ocr_data = run_ocr(image_path)

    # ---------------- MERGE LOGIC ----------------

    final_price = db_price if db_price else ocr_data.get("price", "Not Available")

    output = {
        "Predicted Label": predicted_label,
        "Confidence": confidence_percent,
        "Packaging": packaging_type,
        "Item": item,
        "Subtype": subtype,
        "Brand": brand,

        # Pricing
        "Price": final_price,
        "Expiry Date": ocr_data.get("expiry", db_shelf),

        # Nutrition (DB priority)
        "Calories": db_cal if db_cal else ocr_data.get("calories"),
        "Protein": db_prot if db_prot else ocr_data.get("protein"),
        "Fat": db_fat if db_fat else ocr_data.get("fat"),
        "Carbs": db_carbs if db_carbs else ocr_data.get("carbs"),
        "Fiber": db_fiber if db_fiber else ocr_data.get("fiber"),
        "Sugar": db_sugar if db_sugar else ocr_data.get("sugar"),

        # Extra DB Fields
        "Shelf Life": db_shelf,
        "Storage Advice": db_storage,
        "Health Score": db_health,
        "Dietary Tag": db_diet,
        "Alternative Item": db_alternative
    }

    return output