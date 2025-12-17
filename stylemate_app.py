import streamlit as st
from PIL import Image
import numpy as np
import urllib.parse
import warnings

warnings.filterwarnings("ignore")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StyleMate – AI Stylist",
    page_icon="👗",
    layout="centered"
)

st.title("👗 StyleMate – Your Premium AI Personal Stylist")
st.write(
    "Personalized outfit, bottoms, footwear & accessories based on "
    "**gender, age, body type, skin tone and occasion**."
)

# ---------------- HELPER FUNCTIONS ----------------

def encode_q(q: str) -> str:
    return urllib.parse.quote_plus(q)

def get_shopping_links(keyword: str, gender: str):
    prefix = ""
    if gender == "Woman":
        prefix = "women "
    elif gender == "Man":
        prefix = "men "
    elif gender == "Kid":
        prefix = "kids "

    q = encode_q(prefix + keyword)

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
    r, g, b = arr.mean(axis=(0, 1))
    brightness = (r + g + b) / 3

    if brightness > 200:
        return "Light"
    elif brightness > 140:
        return "Medium"
    elif brightness > 90:
        return "Dark"
    elif brightness > 50:
        return "Deep"

# ---------------- AI-LIKE JEANS PICKER ----------------

def pick_jeans_ai(gender, body_type, occasion):
    if gender == "Woman":
        if body_type == "Pear":
            return ["High-waist wide jeans", "Straight fit jeans"]
        if body_type == "Hourglass":
            return ["Straight fit jeans", "Bootcut jeans"]
        if body_type == "Rectangle":
            return ["Wide leg jeans", "Boyfriend jeans"]
        return ["Relaxed fit jeans", "Straight jeans"]
        if body_type == "Inverted triangle":
            return ["Wide leg jeans", "Boyfriend jeans", "Straight fit jeans", "Bootcut jeans"]
            
    if gender == "Man":
        if body_type == "Athletic":
            return ["Tapered jeans", "Slim fit jeans"]
        if body_type == "Broad":
            return ["Straight fit jeans", "Relaxed fit jeans"]
        return ["Slim fit jeans", "Regular fit jeans"]

    return ["Comfort fit jeans"]

# ---------------- OUTFIT LOGIC ----------------

def get_tops(occasion, gender):
    if "Party" in occasion:
        if gender == "Woman":
            return [
                ("Party dress", "party dress"),
                ("Party wear top", "party top"),
                ("Skirt", "women party skirt"),
            ]
        else:
            return [
                ("Party shirt", "party shirt"),
            ]

    if "Office" in occasion:
        return [("Formal shirt / blouse", "formal wear")]

    if "Traditional" in occasion:
        return [("Ethnic outfit", "ethnic wear")]

    return [("Casual top / t-shirt", "casual wear")]

def get_footwear_and_accessories(occasion, age):
    if age == "Newborn (0–1)":
        return [
            ("Baby booties", "newborn socks"),
            ("Baby cap", "newborn cap"),
        ]

    if "Office" in occasion:
        return [
            ("Formal shoes", "formal shoes"),
            ("Office bag", "office bag"),
            ("Watch", "watch"),
        ]

    if "Party" in occasion:
        return [
            ("Stylish footwear", "party footwear"),
            ("Clutch / sling bag", "party bag"),
            ("Jewellery / watch", "party accessories"),
        ]

    return [
        ("Casual footwear", "casual shoes"),
        ("Backpack / handbag", "fashion bag"),
        ("Sunglasses / watch", "fashion accessories"),
    ]

# ---------------- UI ----------------

st.markdown("## 🎯 Occasion")
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
gender = st.selectbox("Gender", ["Woman", "Man", "Kid"])
age = st.selectbox(
    "Age group",
    ["Newborn (0–1)", "Child (2–12)", "Teen", "Adult", "Senior"]
)

# ---------------- BODY TYPE ----------------

st.markdown("## 🧍 Body Type")

if age == "Newborn (0–1)":
    body_type = "Newborn"
    st.info("👶 Body type skipped for newborns.")
else:
    if gender == "Woman":
        body_type = st.selectbox(
            "Select body type",
            ["Pear", "Apple", "Hourglass", "Rectangle", " Inverted triangle"]
        )
    elif gender == "Man":
        body_type = st.selectbox(
            "Select body type",
            ["Athletic", "Broad", "Rectangle"]
        )
    else:
        body_type = "Child"

# ---------------- SKIN TONE ----------------

st.markdown("## 🎨 Skin Tone")
skin_mode = st.radio("Skin tone input", ["Upload photo", "Manual select"])

if skin_mode == "Upload photo":
    skin_img = st.file_uploader("Upload face or hand image", ["jpg", "png"])
    if skin_img:
        skin_tone = detect_skin_tone_from_image(skin_img)
        st.success(f"Detected skin tone: {skin_tone}")
    else:
        st.stop()
else:
    skin_tone = st.selectbox(
        "Select skin tone",
        ["Light", "Medium", "Tan", "Deep"]
    )

# ---------------- TOP PICK ----------------

st.markdown("## ✨ StyleMate’s AI Picks for You")

st.info(
    f"Based on **{occasion.lower()}**, **{gender.lower()}**, "
    f"**{body_type.lower()} body type**, and **{skin_tone.lower()} skin tone**."
)

items = []

# Tops
items.extend(get_tops(occasion, gender))

# Jeans (2–3 max)
jeans_list = pick_jeans_ai(gender, body_type, occasion)
for j in jeans_list:
    items.append(("Jeans", j))

# Footwear & accessories
items.extend(get_footwear_and_accessories(occasion, age))

# ---------------- DISPLAY ----------------

for label, key in items:
    st.markdown(f"**• {label}**")
    links = get_shopping_links(key, gender)
    cols = st.columns(len(links))
    for col, brand in zip(cols, links):
        col.link_button(brand, links[brand])

st.markdown("---")
st.caption("StyleMate – Rule-based AI Fashion Recommendation MVP")









