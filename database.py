import sqlite3

DB_NAME = "database.db"

def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # Categories Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    )
    """)

    # Grocery Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grocery_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,

        category_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        subtype TEXT,
        local_name TEXT,

        packaging_type TEXT CHECK(packaging_type IN ('Loose','Packaged')) NOT NULL,
        brand TEXT,

        price_range TEXT,

        calories REAL,
        protein REAL,
        fat REAL,
        carbs REAL,
        fiber REAL,
        sugar REAL,

        shelf_life TEXT,
        storage_advice TEXT,

        health_score REAL CHECK(health_score BETWEEN 0 AND 10),
        dietary_tag TEXT,
                   
        alternative_item TEXT,

        FOREIGN KEY (category_id) REFERENCES categories(category_id),
                   
        UNIQUE(item_name, subtype, brand)
    )
                   
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


def insert_unpackaged_items():  
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")  

    # Insert Category
    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        ("Grains",)
    )

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        ("Grains",)
    )
    category_id = cursor.fetchone()[0]

    # ---------- Grains ----------
    grains_data = [
        ("Rice", "Bora", "Bora Saul (বৰা চাউল)", "80-160 per kg", 337, 2.7, 0.3, 81, 1.0, 0.1, "1 year", "Keep in a dry, airtight container away from moisture.", 7, "High carb, energy-dense.", "Sticky Rice"),
        ("Rice", "Joha", "Joha Saul (জোহা চাউল)", "90-180 per kg", 354, 7.9, 0.5, 79, 0.5, 0.2, "12-18 months","Store airtight in a cool, dark place to preserve aroma.", 9, "Antioxidant-rich, easy digestion.", "Gobindobhog Rice"),
        ("Rice", "Basmati", "Basmati Saul (বাসমতী চাউল)", "110-220 per kg", 350, 8.4, 0.8, 78, 1.2, 0.1, "1-2 years", "Store airtight in a cool, dark place to preserve aroma.", 8, "Low GI, diabetic-friendly, gluten-free staple.", "Johua Rice"),
        ("Chira", "Thin","Patol Chira (পাতল চিৰা)", "40-60 per kg", 350, 7.0, 1.0, 77, 1.5, 1.0, "4 months", "Store in airtight jars; highly sensitive to humidity.", 7.5, "Easy-digest, instant energy.", "Oats"),
        ("Chira", "Thick", "Dath Chira (ডাঠ চিৰা)", "55-85 per kg", 353, 7.2, 0.2, 80, 0.7, 0.4, "6 months", "Store in airtight jars; highly sensitive to humidity.", 8, "High-fiber, sustained energy.", "Nylon Poha"),
        ("Puffed Rice", None, "Muri (মুৰি)", "60-90 per kg", 400, 6.3, 0.5, 90, 1.7, 0.2, "4-6 months", "Seal tightly after use to maintain crispness.", 6, "Low-calorie, weight-loss friendly.", "Makhana")
    ]

    for item_name, subtype, local_name, price_range, cal, prot, fat, carb, fiber, sugar, shelf_life, storage_advice, health_score, dietary_tag, alternative_item in grains_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype, local_name,
            packaging_type, brand,
            price_range,
            calories, protein, fat, carbs, fiber, sugar,
            shelf_life, storage_advice,
            health_score, dietary_tag,
            alternative_item
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            category_id,
            item_name,
            subtype,
            local_name,
            "Loose",
            None,
            price_range,
            cal, prot, fat, carb, fiber, sugar,
            shelf_life,
            storage_advice,
            health_score,
            dietary_tag,
            alternative_item
        ))


# -------------------------
# Add New Category: Pulses
# -------------------------

    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        ("Pulses",)
    )

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        ("Pulses",)
    )
    pulses_category_id = cursor.fetchone()[0]

    pulses_data = [

        ("Dal", "Masoor", "Mosur Dal (মসুৰ ডাল)", "80-110 per kg", 350, 24, 1.1, 60, 11, 2, "12-18 months", 8.8, "High-protein, quick-cooking, heart-healthy.", "Chana Dal"),
        ("Dal", "Moong", "Mug Dal (মুগ ডাল)", "90-120 per kg", 348, 24, 1.2, 63, 16, 6, "12-18 months", 9.0, "Easy-to-digest, detox friendly, low-fat.", "Toor Dal"),

        ("Chickpea", "Boot", "Boot (বুট)", "70-100 per kg", 360, 20, 6, 60, 17, 10, "2 years", 8.7, "High-fiber, sustains energy, iron-rich.", "Black Gram (Mati Mah)"),
        ("Chickpea", "Kabuli", "Kabuli Boot (কাবুলি বুট)", "60-90 per kg", 364, 19, 6, 61, 17, 11, "18-24 months", 8.6, "Protein-packed, low-GI, muscle-building.", "Navy Beans"),

        ("Mung Bean", None, "Mug (মুগ)", "100-120 per kg", 347, 24, 1.2, 63, 16, 7, "18-24 months", 9.2, "Antioxidant-rich, nutrient-dense, plant protein.", "Black Gram"),

        ("Dry Peas", None, "Motor (মটৰ)", "80-120 per kg", 341, 25, 1.2, 60, 25, 8, "12-18 months", 9.1, "High-fiber, budget-friendly, gut-health.", "Green Peas"),

        ("Soyabean", None, "Soyabean (ছয়াবিন)", "60-90 per kg", 446, 36, 20, 30, 9, 7, "6-12 months", 8.6, "Complete protein, omega-3, bone-health.", "Paneer")
    ]

    for item_name, subtype, local_name, price_range, cal, prot, fat, carb, fiber, sugar, shelf_life, health_score, dietary_tag, alternative_item in pulses_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype, local_name,
            packaging_type, brand,
            price_range,
            calories, protein, fat, carbs, fiber, sugar,
            shelf_life, storage_advice,
            health_score, dietary_tag,
            alternative_item
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pulses_category_id,
            item_name,
            subtype,
            local_name,
            "Loose",
            None,
            price_range,
            cal, prot, fat, carb, fiber, sugar,
            shelf_life,
            "Store in airtight container in a cool, dry place",
            health_score,   
            dietary_tag,
            alternative_item
        ))



    # -------------------------
    # Add New Category: Fruits
    # -------------------------

    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        ("Fruits",)
    )

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        ("Fruits",)
    )
    fruits_category_id = cursor.fetchone()[0]

    # Insert Fruits Items
    fruits_data = [

        ("Grapes", "White", "Angur(আঙুৰ)", "120-180 per kg", 67, 0.6, 0.4, 17, 0.9, 15,
         "7-10 days", "Store in a perforated bag in the fridge.", 8,
         "Low-sodium, Hydrating, Natural-sugar.", "Gooseberry"),

        ("Grapes", "Black", "Kola Angur (কলা আঙুৰ)", "120-180 per kg", 69, 0.7, 0.2, 18, 0.9, 16,
         "5-7 days", "Keep refrigerated; wash only immediately before eating.", 9,
         "Antioxidant-rich, Heart-healthy, Low-fat.", "Jamun"),

        ("Banana", "Seeni", "Seeni Kol(চিনি কল)", "30-50 per akhi", 89, 1.1, 0.3, 23, 2.6, 12,
         "3-5 days", "Room temperature; away from direct sunlight.", 8,
         "High-potassium, Pre-workout energy.", "Papaya"),

        ("Banana", "Bhim", "Bhim Kol(ভীম কল)", "30-50 per akhi", 110, 1.3, 0.33, 33, 2.8, 12.2,
         "7-10 days", "Room temperature; away from direct sunlight.", 8,
         "High-potassium, Pre-workout energy.", "Papaya"),

        ("Apple", None, "Apel(আপেল)", "150-250 per kg", 52, 0.3, 0.2, 14, 2.4, 10,
         "2-4 weeks", "Refrigerate in a crisper drawer for freshness.", 9,
         "High-fiber, Low-GI, Heart-healthy.", "Pear"),

        ("Gooseberry", None, "Amolokhi(আমলখি)", "120-180 per kg", 44, 0.9, 0.6, 10, 4.3, 0.0,
         "1-2 weeks", "Cool, dry place; refrigerate for longevity.", 10,
         "Vitamin-C Powerhouse, Immunity-booster.", "Star Fruit"),

        ("Jujube", None, "Bogori(বগৰী)", "60-100 per kg", 79, 1.2, 0.2, 20, 1.5, 0.0,
         "1 week", "Spread out in a cool, dry tray.", 9,
         "High-antioxidant, Traditional-medicine.", "Plum"),

        ("Elephant Apple", None, "Ou-Tenga(ঔ-টেঙা)", "5-20 per piece", 59, 0.8, 0.2, 15, 2.5, 0.3,
         "1-2 weeks", "Store in fridge; use quickly once cut.", 9,
         "Gut-healthy, High-fiber, Sour-tangy.", "Rhubarb"),
    ]

    for item_name, subtype, local_name, price_range, cal, prot, fat, carb, fiber, sugar, shelf_life, storage_advice, health_score, dietary_tag, alternative_item in fruits_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype, local_name,
            packaging_type, brand,
            price_range,
            calories, protein, fat, carbs, fiber, sugar,
            shelf_life, storage_advice,
            health_score, dietary_tag,
            alternative_item
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)
        """, (
            fruits_category_id,
            item_name,
            subtype,
            local_name,
            "Loose",
            None,
            price_range,
            cal, prot, fat, carb, fiber, sugar,
            shelf_life,
            storage_advice,
            health_score,
            dietary_tag,
            alternative_item
        ))



    # -------------------------
    # Add New Category: Vegetables
    # -------------------------

    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        ("Vegetables",)
    )

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        ("Vegetables",)
    )
    vegetables_category_id = cursor.fetchone()[0]

    vegetables_data = [

        ("Cabbage", None, "Bondhakobi (বন্ধাকবি)", "20-40 per kg", 25, 1.3, 0.1, 6, 2.5, 3.2,
         "2-3 weeks", "Keep refrigerated whole.", 8, "High Fiber, Low Calorie", "Bok Choy"),

        ("Onion", None,"Piyaj (পিয়াঁজ)", "25-50 per kg", 40, 1.1, 0.1, 9.3, 1.1, 4.2,
         "1-2 months", "Store in dry ventilated place.", 7.5, "Antioxidant Rich, Heart Friendly", "Shallots"),

        ("Potato", None, "Alu (আলু)", "20-40 per kg", 77, 2, 0.1, 17, 2.2, 0.8,
         "1-2 months", "Store in cool dark place.", 7, "Energy Rich, Gluten Free", "Yam"),

        ("Tomato", None, "Bilahi (বিলাহী)", "20-60 per kg", 18, 0.9, 0.2, 3.9, 1.2, 2.6,
         "1 week", "Keep at room temperature; refrigerate when ripe.", 9, "Lycopene Rich, Low Calorie", "Tanmarind"),

        ("Cauliflower", None, "Phulkobi (ফুলকবি)", "30-70 per kg", 25, 1.9, 0.3, 5, 2, 1.9,
         "1 week", "Keep refrigerated in perforated bag.", 9, "Low Carb, High Fiber", "Broccoli"),

        ("Carrot", None, "Gajor (গাজৰ)", "30-60 per kg", 41, 0.9, 0.2, 10, 2.8, 4.7,
         "2-3 weeks", "Refrigerate; remove greens.", 9, "Vitamin A Rich, Antioxidant", "Beetroot"),

        ("Raddish", None,"Mulā (মূলা)", "30-60 per kg", 16, 0.7, 0.1, 3.4, 1.6, 1.9,
         "1-2 weeks", "Refrigerate in perforated bag; remove leaves.", 8, "Low Calorie, High Fiber", "Turnip"),

        ("Mushroom", None, "Kathfula (কাঠফুলা)", "200-350 per kg", 22, 3.1, 0.3, 3.3, 1, 2,
         "3-5 Days", "Keep in paper bag in refrigerator.", 9, "High Protein, Low Calorie", "Soya Chunks"),

        ("Roselle", None, "Tengamora (টেঙামৰা)", "20-50 per kg", 37, 1, 0.6, 7, 2.5, 0.5,
         "3-5 Days", "Refrigerate in moisture-free bag.", 8, "Vitamin Rich, Antioxidant Source", "Gongura"),

        ("Sichuan Pepper Leaves", None, "Mejenga (মেজেঙ্গা)", "20-40 per bunch", 35, 2, 0.5, 6, 3, 0.5,
         "4-6 Days", "Store refrigerated; avoid moisture.", 8, "Herbal, High Fiber", "Black pepper"),

        ("Dhania", None, "Dhaniya Paat (ধনীয়া পাতা)", "20-40 per bunch", 23, 2.1, 0.5, 3.7, 2.7, 0.7,
         "5-7 Days", "Wrap in damp cloth; refrigerate.", 9, "Detox Friendly, Nutrient Rich", "Mint"),

        ("Taro Leaves", None, "Kosu Paat (কচু পাতা)", "30-60 per bunch", 42, 4, 0.7, 6.7, 3.7, 0.3,
         "2-3 Days", "Refrigerate; cook thoroughly.", 8, "Iron Rich, High Fiber", "Spinach"),

        ("Taro Root", None, "Kosu (কচু)", "40-80 per kg", 112, 1.5, 0.2, 26, 4.1, 0.5,
         "2-3 Weeks", "Store in cool dry place.", 7.5, "Energy Rich, High Carb", "Cassava"),

        ("Brinjal", None, "Bengena (বেঙেনা)", "30-70 per kg", 25, 1, 0.2, 6, 3, 3.5,
         "4-6 Days", "Refrigerate; avoid bruising.", 8, "Low Calorie, High Fiber", "Zucchini"),

        ("Pumpkin", None, "Rangaa Lau (ৰঙা লাউ)", "20-50 per kg", 26, 1, 0.1, 6.5, 0.5, 2.8,
         "1-2 Months", "Store whole in cool dry place.", 8, "Vitamin A Rich, Low Fat", "Squash"),

        ("Bahok Teeta", None, "Baheka (বাহেকা)", "30-70 per bunch", 10, 2, 0.5, 5, 2, 0.5,
         "3-4 Days", "Refrigerate; consume fresh.", 8, "Nutrient Dense, Herbal Leaf", "Neem leaves"),

        ("Cassava", None, "Gaas Aalu (গছ আলু)", "30-50 per kg", 160, 1.4, 0.3, 38, 1.8, 1.7,
        "5–7 days", "Store in a cool, dry place", 7, "Gluten_free, high_carb", "Sweet potato"),

        ("Fiddlehead Fern", None, "Dhekia (ঢেকীয়া)", "20-30 per bunch", 34, 4.3, 0.4, 6.5, 3.6, 0.5,
         "1-2 Days", "Store in breathable bag in refrigerator", 8.5, "Nutrient Dense, Herbal Leaf", "Spinach")
    ]

    for item_name, subtype, local_name, price_range, cal, prot, fat, carb, fiber, sugar, shelf_life, storage_advice, health_score, dietary_tag, alternative_item in vegetables_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype, local_name,
            packaging_type, brand,
            price_range,
            calories, protein, fat, carbs, fiber, sugar,
            shelf_life, storage_advice,
            health_score, dietary_tag,
            alternative_item
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vegetables_category_id,
            item_name,
            subtype,
            local_name,
            "Loose",
            None,
            price_range,
            cal, prot, fat, carb, fiber, sugar,
            shelf_life,
            storage_advice,
            health_score,
            dietary_tag,
            alternative_item
        ))


    # -------------------------
    # Add New Category: Fresh Herbs
    # -------------------------

    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        ("Fresh herbs",)
    )

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        ("Fresh herbs",)
    )
    herbs_category_id = cursor.fetchone()[0]

    herbs_data = [
        ("Mint", None, "Pudina (পদিনা)", "10-30 per bunch", 44, 3.3, 0.9, 8.4, 6.8, 0.9,
         "3-5 Days", "Fridge in damp paper towel or water jar.", 9, "Natural Detoxifier", "Dhania"),

        ("Shunk Vine", None, "Vedailata (ভেদাইলতা)", "10-15 per bunch", 35, 2.5, 0.5, 6.0, 4.0, 0.3,
         "2-3 Days", "Use fresh or store leaves in airtight containers.", 9.5, "Gastro-Protective", "Curry leaves"),

        ("Pennywort", None, "Manimuni (মানিমুনি)", "15-25 per bunch", 36, 2.0, 0.1, 6.5, 3.5, 0.4,
         "3-4 Days", "Keep roots moist; store in a sealed plastic bag.", 9.7, "Neuro-Protective", "Spinach")
    ]

    for item_name, subtype, local_name, price_range, cal, prot, fat, carb, fiber, sugar, shelf_life, storage_advice, health_score, dietary_tag, alternative_item in herbs_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype, local_name,
            packaging_type, brand,
            price_range,
            calories, protein, fat, carbs, fiber, sugar,
            shelf_life, storage_advice,
            health_score, dietary_tag,
            alternative_item
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            herbs_category_id,
            item_name,
            subtype,
            local_name,
            "Loose",
            None,
            price_range,
            cal, prot, fat, carb, fiber, sugar,
            shelf_life,
            storage_advice,
            health_score,
            dietary_tag,
            alternative_item
        ))


    # -------------------------
    # Add New Category: Spices
    # -------------------------

    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        ("Spices",)
    )

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        ("Spices",)
    )
    spices_category_id = cursor.fetchone()[0]

    spices_data = [

        ("Sesame Seed", None,  "Til (তিল)", "120-180 per kg", 570, 19, 55, 17, 13, 0.5,
         "6–12 months", "Airtight container in a cool, dark place.", 8.8,
         "Keto-friendly, Gluten-free, High-protein.", "Peanuts"),

        ("Black Pepper", None, "Jaluk (জালুক)", "600-800 per kg", 250, 10, 3.3, 64, 25, 0.6,
         "2–3 years", "Store whole in airtight containers away from moisture.", 8.5,
         "Paleo, Keto-friendly, Low-calorie.", "Pipali"),

        ("Garlic", None, "Nohoru (নহৰু)", "120-250 per kg", 33, 6.4, 0.4, 33, 2.1, 5,
         "3-5 months", "Store in a cool, dry, well-ventilated place.", 8,
         "Heart-healthy, Anti-inflammatory, Low-fat.", "Chives")
    ]

    for item_name, subtype, local_name, price_range, cal, prot, fat, carb, fiber, sugar, shelf_life, storage_advice, health_score, dietary_tag, alternative_item in spices_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype, local_name,
            packaging_type, brand,
            price_range,
            calories, protein, fat, carbs, fiber, sugar,
            shelf_life, storage_advice,
            health_score, dietary_tag,
            alternative_item
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            spices_category_id,
            item_name,
            subtype,
            local_name,
            "Loose",
            None,
            price_range,
            cal, prot, fat, carb, fiber, sugar,
            shelf_life,
            storage_advice,
            health_score,
            dietary_tag,
            alternative_item
        ))


    # -------------------------
    # Add New Category: Seafood
    # -------------------------

    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        ("Seafood",)
    )

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        ("Seafood",)
    )
    seafood_category_id = cursor.fetchone()[0]

    seafood_data = [

        ("Snail", None, "Hamuk (হামুক)", "200-350 per kg", 90, 16.0, 1.4, 2.0, 0.0, 0.0,
         "2-3 Days", "Store in breathable container; keep cool and damp.", 9,
         "High-Protein, Iron-Rich", "Mushroom")
    ]

    for item_name, subtype, local_name, price_range, cal, prot, fat, carb, fiber, sugar, shelf_life, storage_advice, health_score, dietary_tag, alternative_item in seafood_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype, local_name,
            packaging_type, brand,
            price_range,
            calories, protein, fat, carbs, fiber, sugar,
            shelf_life, storage_advice,
            health_score, dietary_tag,
            alternative_item
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            seafood_category_id,
            item_name,
            subtype,
            local_name,
            "Loose",
            None,
            price_range,
            cal, prot, fat, carb, fiber, sugar,
            shelf_life,
            storage_advice,
            health_score,
            dietary_tag,
            alternative_item
        ))


    # -------------------------
    # Add New Category: Speciality food
    # -------------------------

    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        ("Specialty Food",)
    )

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        ("Specialty Food",)
    )
    speciality_food_category_id = cursor.fetchone()[0]

    speciality_food_data = [

        ("Silkworm", None, "Polu (পলু)", "400-700 per kg", 450, 50, 26, 7, 3, 0.2,
         "1-2 Days", "Keep fresh pupae refrigerated; consume within 24 hours.", 9,
         "High-protein, Keto-friendly, Paleo, Sustainable-resource.", "Mushroom")
    ]

    for item_name, subtype, local_name, price_range, cal, prot, fat, carb, fiber, sugar, shelf_life, storage_advice, health_score, dietary_tag, alternative_item in speciality_food_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype, local_name,
            packaging_type, brand,
            price_range,
            calories, protein, fat, carbs, fiber, sugar,
            shelf_life, storage_advice,
            health_score, dietary_tag,
            alternative_item
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            speciality_food_category_id,
            item_name,
            subtype,
            local_name,
            "Loose",
            None,
            price_range,
            cal, prot, fat, carb, fiber, sugar,
            shelf_life,
            storage_advice,
            health_score,
            dietary_tag,
            alternative_item
        ))


    conn.commit()
    conn.close()

    print("Unpackaged items inserted successfully.")



def insert_packaged_items():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    categories = ["Dairy", "Biscuits", "Oil", "Chips", "Bhujia"]

    for cat in categories:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
            (cat,)
        )

    def get_category_id(name):
        cursor.execute("SELECT category_id FROM categories WHERE category_name = ?", (name,))
        return cursor.fetchone()[0]

    dairy_id = get_category_id("Dairy")
    biscuits_id = get_category_id("Biscuits")
    oil_id = get_category_id("Oil")
    chips_id = get_category_id("Chips")
    bhujia_id = get_category_id("Bhujia")

    packaged_data = [

    # ---------------- Milk ----------------
    (dairy_id, "Milk", "Toned", "Amul", 9,
     "High calcium, protein-rich.", "Soy Milk",
     "Keep refrigerated below 4°C."),

    # ---------------- Biscuits ----------------
    (biscuits_id, "Biscuit", "Cream", "Oreo", 6,
     "High sugar snack.", "Digestive Biscuit",
     "Store in cool dry place."),

    (biscuits_id, "Biscuit", "Cream", "Bounce", 6,
     "Sweet cream biscuit.", "Digestive Biscuit",
     "Store in cool dry place."),

    (biscuits_id, "Biscuit", "Digestive", "Britannia", 8.5,
     "High fiber biscuit.", "Oats Biscuit",
     "Keep airtight after opening."),

    # ---------------- Oil ----------------
    (oil_id, "Oil", "Mustard", "Nivaz", 8.5,
     "Traditional heart-friendly oil.", "Soyabean Oil",
     "Store away from sunlight."),

    (oil_id, "Oil", "Mustard", "Anupam", 8,
     "Cold pressed mustard oil.", "Soyabean Oil",
     "Store away from sunlight."),

    (oil_id, "Oil", "Soyabean", None, 7.5,
     "Refined cooking oil.", "Mustard Oil",
     "Keep tightly sealed."),

    # ---------------- Chips ----------------
    (chips_id, "Chips", None, "Bingo", 6,
     "Fried snack.", "Baked Chips",
     "Store airtight."),

    (chips_id, "Chips", None, "Kurkure", 5.5,
     "Spicy crunchy snack.", "Roasted Makhana",
     "Store airtight."),

    (chips_id, "Chips", None, "Noodles", 5,
     "Masala snack.", "Puffed Rice",
     "Store airtight."),

    (chips_id, "Chips", None, "Tedhe Medhe", 5,
     "Fried wheat snack.", "Roasted Corn",
     "Store airtight."),

    (chips_id, "Chips", None, "Crunchy Bytes", 6,
     "Crispy snack.", "Khakhra",
     "Store airtight."),

    # ---------------- Bhujia ----------------
    (bhujia_id, "Bhujia", None, "Tana Bana", 5,
     "Deep fried namkeen.", "Roasted Chana",
     "Store airtight.")
]

    for category_id, item_name, subtype, brand, health_score, dietary_tag, alternative_item, storage_advice in packaged_data:
        cursor.execute("""
        INSERT OR IGNORE INTO grocery_items (
            category_id, item_name, subtype,
            packaging_type, brand,
            health_score, dietary_tag,
            alternative_item, storage_advice
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            category_id,
            item_name,
            subtype,
            "Packaged",
            brand,
            health_score,
            dietary_tag,
            alternative_item,
            storage_advice
        ))

    conn.commit()
    conn.close()
    print("Packaged items inserted successfully.")


if __name__ == "__main__":
    initialize_database()
    insert_unpackaged_items()
    insert_packaged_items()
