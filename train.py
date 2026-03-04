import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# ---------------- CONFIG ----------------

TRAIN_DIR = r"C:\Users\91876\OneDrive\Documents\AI GROCERY RECOGNITION\AI-GROCERY-ITEM-RECOGNITION\Grocery Dataset\train data"
VAL_DIR = r"C:\Users\91876\OneDrive\Documents\AI GROCERY RECOGNITION\AI-GROCERY-ITEM-RECOGNITION\Grocery Dataset\validation data"
TEST_DIR = r"C:\Users\91876\OneDrive\Documents\AI GROCERY RECOGNITION\AI-GROCERY-ITEM-RECOGNITION\Grocery Dataset\test data"

MODEL_SAVE_PATH = "models/grocery_model.pth"

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15
LR = 0.0005
PATIENCE = 5

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- CUSTOM DATASET ----------------

class GroceryDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.samples = []
        self.transform = transform

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith((".jpg", ".png", ".jpeg")):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, root_dir)
                    label = relative_path.replace(os.sep, "_")
                    self.samples.append((full_path, label))

        self.classes = sorted(list(set([s[1] for s in self.samples])))
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        image_path, label = self.samples[idx]
        image = Image.open(image_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        label_idx = self.class_to_idx[label]
        return image, label_idx

# ---------------- TRANSFORMS ----------------

train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(25),
    transforms.ColorJitter(0.4, 0.4, 0.4),
    transforms.RandomAffine(degrees=15, translate=(0.1, 0.1)),
    transforms.ToTensor()
])

eval_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor()
])

# ---------------- LOAD DATA ----------------

train_dataset = GroceryDataset(TRAIN_DIR, transform=train_transform)
val_dataset = GroceryDataset(VAL_DIR, transform=eval_transform)
test_dataset = GroceryDataset(TEST_DIR, transform=eval_transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

num_classes = len(train_dataset.classes)
print("Total Classes:", num_classes)

# ---------------- MODEL ----------------

model = models.efficientnet_b0(pretrained=True)

# Freeze backbone (important for small dataset)
for param in model.features.parameters():
    param.requires_grad = False

in_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(in_features, num_classes)

model = model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=1e-4)

# ---------------- TRAINING ----------------

best_val_acc = 0
early_stop_counter = 0

for epoch in range(EPOCHS):

    model.train()
    train_loss = 0
    train_preds = []
    train_labels = []

    for images, labels in tqdm(train_loader):
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        _, preds = torch.max(outputs, 1)

        train_preds.extend(preds.cpu().numpy())
        train_labels.extend(labels.cpu().numpy())

    train_acc = accuracy_score(train_labels, train_preds)

    # ---- VALIDATION ----
    model.eval()
    val_preds = []
    val_labels = []

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)

            val_preds.extend(preds.cpu().numpy())
            val_labels.extend(labels.cpu().numpy())

    val_acc = accuracy_score(val_labels, val_preds)

    print(f"\nEpoch [{epoch+1}/{EPOCHS}]")
    print(f"Train Loss: {train_loss/len(train_loader):.4f}")
    print(f"Train Accuracy: {train_acc:.4f}")
    print(f"Validation Accuracy: {val_acc:.4f}")

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        os.makedirs("models", exist_ok=True)
        torch.save(model.state_dict(), MODEL_SAVE_PATH)
        print("Model Saved (Improved)")
        early_stop_counter = 0
    else:
        early_stop_counter += 1

    if early_stop_counter >= PATIENCE:
        print("Early Stopping Triggered")
        break

print("\nTraining Finished")
print("Best Validation Accuracy:", best_val_acc)

# ---------------- TEST EVALUATION ----------------

print("\nEvaluating on Test Set...")

model.load_state_dict(torch.load(MODEL_SAVE_PATH))
model.eval()

test_preds = []
test_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)

        test_preds.extend(preds.cpu().numpy())
        test_labels.extend(labels.cpu().numpy())

test_acc = accuracy_score(test_labels, test_preds)
print("Final Test Accuracy:", test_acc)

# ---------------- CONFUSION MATRIX ----------------

cm = confusion_matrix(test_labels, test_preds)

plt.figure(figsize=(14,12))
sns.heatmap(cm,
            cmap="Blues",
            xticklabels=train_dataset.classes,
            yticklabels=train_dataset.classes)

plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# ---------------- CLASSIFICATION REPORT ----------------

report = classification_report(test_labels, test_preds,
                               target_names=train_dataset.classes)

print("\nDetailed Classification Report:\n")
print(report)

with open("classification_report.txt", "w") as f:
    f.write(report)