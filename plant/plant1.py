import streamlit as st
from plantdoc_predictor import Predictor
from PIL import Image
import tempfile
import os
from google import genai
import json
import re

# -----------------------------
# GEMINI CONFIG
# -----------------------------
API_KEY = "AIzaSyCPgUjAXujgdklNeU5V7F8bBwU_dKShieM"   # 🔑 Replace with your real Gemini key
client = genai.Client(api_key=API_KEY)

# -----------------------------
# DEFINE AVAILABLE MODELS
# -----------------------------
def list_available_models():
    return ["inceptionv3", "resnet50", "mobilenetv2"]

# -----------------------------
# STREAMLIT PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="🌿 Plant Disease Detector", page_icon="🌱", layout="wide")

# 🎨 Background Gradient
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom right, black, #006994, #004f63);
        color: white !important;
    }
    /* Reduce image size */
    .uploaded-img img {
        max-width: 60% !important;
        border-radius: 15px;
        box-shadow: 0px 0px 15px rgba(255,255,255,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🌿 Plant Disease Prediction App")
st.markdown("Upload a leaf image to detect possible crop disease using AI.")

# -----------------------------
# SIDEBAR CONFIG
# -----------------------------
st.sidebar.header("⚙️ Settings")
available_models = list_available_models()
model_choice = st.sidebar.selectbox("Select AI Model", available_models, index=0)

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model(model_name):
    st.sidebar.info(f"🔄 Loading {model_name} model...")
    predictor = Predictor(model_name=model_name, verbose=False)
    return predictor

predictor = load_model(model_choice)
st.sidebar.success(f"✅ {model_choice} model loaded successfully!")

# -----------------------------
# GEMINI FUNCTION
# -----------------------------
def get_disease_explanation_and_remedies(disease_name):
    """
    Ask Gemini for a short explanation and 2 remedies for a given plant disease.
    """
    prompt = f"""
    You are an expert plant pathologist.
    Explain briefly about the disease '{disease_name}' in simple terms.
    Then provide exactly TWO effective remedies for it.
    Return strictly in JSON format as shown below:
    {{
        "explanation": "short paragraph explaining the disease",
        "remedies": ["remedy 1", "remedy 2"]
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[{"role": "user", "parts": [{"text": prompt}]}]
    )

    raw_text = getattr(response, "text", "").strip()

    # Clean JSON and parse
    try:
        cleaned = re.sub(r"```json|```", "", raw_text).strip()
        data = json.loads(cleaned)
        return data
    except Exception as e:
        st.error(f"⚠️ Gemini JSON parse error: {e}")
        st.write("Raw Gemini Output:", raw_text)
        return {
            "explanation": "No explanation available.",
            "remedies": ["Try again later.", "Ensure correct disease name."]
        }

# -----------------------------
# MAIN UI
# -----------------------------
uploaded_image = st.file_uploader("📸 Upload a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display uploaded image with controlled size
    image = Image.open(uploaded_image)
    st.markdown('<div class="uploaded-img">', unsafe_allow_html=True)
    st.image(image, caption="Uploaded Leaf Image", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        image.save(tmp_file.name)
        image_path = tmp_file.name

    # Predict button
    if st.button("🔍 Predict Disease"):
        with st.spinner("Analyzing the image... please wait ⏳"):
            result = predictor.predict(image_path)

        # Display prediction result
        st.success("✅ Prediction Complete!")

        st.markdown("### 🧾 Prediction Result")
        st.write(f"**Predicted Class:** {result['label']}")
        st.write(f"**Confidence:** {result['confidence'] * 100:.2f}%")
        st.write(f"**Model Used:** {result['model']}")

        # Top 3 predictions if available
        if "top3" in result:
            st.markdown("### 🏆 Top-3 Predictions")
            for label, conf in result["top3"].items():
                st.write(f"- **{label}** → {conf * 100:.2f}%")

        # -----------------------------
        # Gemini Explanation + Remedies
        # -----------------------------
        st.markdown("### 🌿 Disease Details & Remedies")

        with st.spinner("🧠 Fetching details..."):
            gemini_output = get_disease_explanation_and_remedies(result["label"])

        # Explanation
        st.markdown(f"**💬 About the Disease:**")
        st.info(gemini_output["explanation"])

        # Remedies Accordion
        with st.expander("💡 Remedies (click to view)"):
            for i, remedy in enumerate(gemini_output["remedies"], 1):
                st.write(f"**Remedy {i}:** {remedy}")

        # Delete temp file
        os.remove(image_path)

else:
    st.info("👆 Upload a leaf image to begin prediction.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("<center>Developed with ❤️ using Helix Brain </center>", unsafe_allow_html=True)