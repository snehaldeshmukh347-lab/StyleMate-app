import streamlit as st
from PIL import Image
import numpy as np
import urllib.parse
import os
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StyleMate – AI Stylist",
    page_icon="👗",
    layout="centered"
)

st.title("👗 StyleMate – Your Premium AI Personal Stylist")
st.write(
    "Personalized outfit, footwear & accessory recommendations based on "
    "**body type, gender, age, skin tone and occasion**."
)

# ---------------- HELPER FUNCTIONS ----------------

def encode_q(q: str) -> str:
    return urllib.parse.quote_plus(q)

def get_shopping_links(keyword: str, gender: str):
    g = gender.lower()
    if g == "woman":
        keyword = "women " + keyword
    elif g == "man":
        keyword = "men " + keyword
    elif g == "kid":
        keyword = "kids " + keyword

    q = encode_q(keyword)

    return {
        "Amazon": f"https://www.amazon.in/s?k={q}",
        "Myntra": f"https://www.myntra.com/{q}",
        "Ajio": f"https://www.ajio.com/search/?text={q}",
        "ZARA": f"https://www.zara.com/in/en/search?searchTerm={q}",
        "H&M": f"https://www2.hm.com/en_in/search-results.html?q={q}",
    }

def detect_skin_tone_from_image(img_file):
    img = Image.open(img_file).convert("RGB")
    arr = np.array(img)

    h, w, _ = arr.shape
    center = arr[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
    r, g, b = center.mean(axis=(0, 1))
    brightness = (r + g + b) / 3

    if brightness > 200:
        return "Light"
    elif brightness > 140:
        return "Medium"
    elif brightness > 90:
        return "Tan"
    else:
        return "Deep"

def detect_body_type_from_photo(img_file):
    img = Image.open(img_file).convert("RGB")
    arr = np.array(img)

    with mp_pose.Pose(static_image_mode=True) as pose:
        res = pose.process(arr)

    if not res.pose_landmarks:
        return None

    lm = res.pose_landmarks.landmark
    sh = abs(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x -
             lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x)
    hp = abs(lm[mp_pose.PoseLandmark.RIGHT_HIP.value].x -
             lm[mp_pose.PoseLandmark.LEFT_HIP.value].x)

    if hp > sh * 1.08:
        return "pear"
    elif sh > hp * 1.08:
        return "inverted_triangle"
    else:
        return "rectangle"

def calculate_body_type(chest, waist, hips):
    if hips / waist > 1.15:
        return "pear"
    elif chest / waist > 1.15:
        return "inverted_triangle"
    elif abs(chest - hips) <= 5:
        return "hourglass"
    elif waist > (chest + hips) * 0.45:
        return "apple"
    else:
        return "rectangle"

# ---------------- RECOMMENDATION LOGIC ----------------

def get_outfit_ideas(occasion, age):
    if age == "Newborn (0–1)":
        return [("Cotton onesie", "newborn cotton onesie")]

    if "Office" in occasion:
        return [("Formal shirt / blouse", "formal wear")]
    if "Traditional" in occasion:
        return [("Ethnic wear set", "ethnic wear")]
    return [("Casual top / t-shirt", "casual top")]

def get_extras(occasion, age):
    if age == "Newborn (0–1)":
        return [
            ("Soft baby booties", "newborn socks"),
            ("Cotton cap", "newborn cap"),
        ]

    if "Office" in occasion:
        return [
            ("Formal shoes", "formal shoes"),
            ("Minimal office bag", "office bag"),
        ]

    return [
        ("Sneakers / heels", "trendy footwear"),
        ("Sling bag", "fashion bag"),
    ]

# ---------------- UI ----------------

st.markdown("## 🎯 Occasion")
st.divider()
occasion = st.selectbox(
    "Select occasion",
    [
        "Casual outing",
        "Office / Formal",
        "Party / Night out",
        "Traditional / Festival / Wedding",
    ],
)

st.markdown("## 👤 User Profile")
st.divider()
gender = st.selectbox("Gender", ["Woman", "Man", "Kid"])
age = st.selectbox(
    "Age group",
    ["Newborn (0–1)", "Child (2–12)", "Teen", "Adult", "Senior"]
)

# ---------------- BODY TYPE ----------------

st.markdown("## 🧍 Body Type")
st.divider()

body_type = None

if age == "Newborn (0–1)":
    body_type = "newborn"
    st.info("👶 Body type is skipped for newborns.")
else:
    mode = st.radio("Input method", ["Upload photo", "Manual"])

    if mode == "Upload photo":
        img = st.file_uploader("Upload full body image", ["jpg", "png"])
        if img:
            body_type = detect_body_type_from_photo(img)
            if body_type:
                st.success(f"Detected body type: {body_type}")
            else:
                st.warning("Could not detect body type clearly.")
    else:
        chest = st.number_input("Chest (cm)", 20, 150, 90)
        waist = st.number_input("Waist (cm)", 20, 150, 70)
        hips = st.number_input("Hips (cm)", 20, 160, 95)
        body_type = calculate_body_type(chest, waist, hips)
        st.success(f"Detected body type: {body_type}")

if body_type is None:
    st.warning("Please complete body type input to continue.")
    st.stop()

# ---------------- SKIN TONE ----------------

st.markdown("## 🎨 Skin Tone")
st.divider()

skin_tone = None
skin_mode = st.radio("Skin tone input", ["Upload photo", "Manual select"])

if skin_mode == "Upload photo":
    skin_img = st.file_uploader(
        "Upload face or hand image",
        ["jpg", "png"],
        key="skin"
    )
    if skin_img:
        skin_tone = detect_skin_tone_from_image(skin_img)
        st.success(f"Detected skin tone: {skin_tone}")
else:
    skin_tone = st.selectbox(
        "Select skin tone",
        ["Light", "Medium", "Tan", "Deep"]
    )

if skin_tone is None:
    st.warning("Please complete skin tone input to continue.")
    st.stop()

# ---------------- TOP PICK ----------------

st.markdown("## ✨ StyleMate’s Top Pick for You")
st.divider()

st.info(
    f"This recommendation is selected based on **{occasion.lower()}**, "
    f"**{age.lower()}**, and **{skin_tone.lower()} skin tone**."
)

items = get_outfit_ideas(occasion, age) + get_extras(occasion, age)

for label, key in items:
    st.markdown(f"**• {label}**")
    links = get_shopping_links(key, gender)
    cols = st.columns(5)
    for col, brand in zip(cols, links):
        col.link_button(brand, links[brand])

st.markdown("---")
st.caption(
    "StyleMate is an academic prototype demonstrating rule-based AI "
    "fashion recommendation logic."
)

