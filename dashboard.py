import streamlit as st
from PIL import Image
from inference import predict

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Grocery Intelligence Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 AI-Based Grocery Recognition & Intelligence System")
st.markdown("EfficientNet-B0 • Database Intelligence • OCR Integration • Confidence Scoring")
st.divider()

# =====================================================
# DISPLAY FUNCTION
# =====================================================

def display_results(image_path):

    col1, col2 = st.columns([1, 1])

    # LEFT SIDE — IMAGE
    with col1:
        image = Image.open(image_path).convert("RGB")
        st.image(image, use_container_width=True)

    # RIGHT SIDE — RESULTS
    with col2:

        with st.spinner("🔍 Running AI Inference..."):
            result = predict(image_path)

        confidence = result.get("Confidence", 0)

        # ---------------- UNKNOWN ----------------

        if result.get("Item") == "Unknown":
            st.error("⚠️ UNKNOWN")
            st.write(f"Confidence: {confidence}%")
            st.progress(confidence / 100)
            return

        # ---------------- CONFIDENCE ----------------

        st.subheader("📊 Model Confidence")
        st.write(f"Confidence: **{confidence}%**")
        st.progress(confidence / 100)

        st.success("✅ Grocery Item Detected")

        st.divider()

        # ---------------- ITEM INFO ----------------

        st.subheader("🔎 Item Identification")
        st.write("**Packaging Type:**", result.get("Packaging", "-"))
        st.write("**Item:**", result.get("Item", "-"))
        st.write("**Subtype:**", result.get("Subtype", "-"))
        st.write("**Brand:**", result.get("Brand", "-"))

        st.divider()

        # ---------------- PRICING ----------------

        st.subheader("💰 Pricing & Shelf Info")
        st.write("**Price:**", result.get("Price", "Not Available"))
        st.write("**Shelf Life:**", result.get("Shelf Life", "Not Available"))
        st.write("**Expiry Date (OCR):**", result.get("Expiry Date", "Not Available"))

        st.divider()

        # ---------------- NUTRITION ----------------

        st.subheader("🥗 Nutrition Information")

        st.write("Calories:", result.get("Calories", "-"))
        st.write("Protein:", result.get("Protein", "-"))
        st.write("Fat:", result.get("Fat", "-"))
        st.write("Carbohydrates:", result.get("Carbs", "-"))
        st.write("Fiber:", result.get("Fiber", "-"))
        st.write("Sugar:", result.get("Sugar", "-"))

        st.divider()

        # ---------------- HEALTH ----------------

        st.subheader("❤️ Health & Storage")

        health_score = result.get("Health Score")

        if health_score:
            st.write(f"Health Score: {health_score}/10")
            st.progress(float(health_score) / 10)
        else:
            st.write("Health Score: Not Available")

        st.write("**Dietary Tag:**", result.get("Dietary Tag", "-"))
        st.write("**Storage Advice:**", result.get("Storage Advice", "-"))

        st.divider()

        # ---------------- ALTERNATIVE ----------------

        st.subheader("🔄 Alternative Recommendation")
        st.write(result.get("Alternative Item", "-"))

# =====================================================
# TABS STRUCTURE
# =====================================================

tabs = st.tabs([
    "📂 Upload Image",
    "📷 Camera Capture",
    "⚡ Quick Scan"
])

# =====================================================
# TAB 1 — UPLOAD
# =====================================================

with tabs[0]:
    st.subheader("Upload Grocery Image")

    uploaded_file = st.file_uploader(
        "Choose Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        display_results(uploaded_file)

# =====================================================
# TAB 2 — CAMERA
# =====================================================

with tabs[1]:
    st.subheader("Capture Grocery Item")

    cam_img = st.camera_input("Take a Picture")

    if cam_img:
        display_results(cam_img)

# =====================================================
# TAB 3 — QUICK SCAN
# =====================================================

with tabs[2]:
    st.subheader("Instant Scan Mode")

    quick_img = st.camera_input("Scan Item")

    if quick_img:
        display_results(quick_img)