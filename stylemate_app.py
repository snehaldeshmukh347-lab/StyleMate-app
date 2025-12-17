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
        return "Tan"
    else:
        return "Deep"

# ---------------- JEANS AI (UNCHANGED) ----------------

def pick_jeans_ai(gender, body_type):
    if gender == "Woman":
        if body_type == "Pear":
            return ["High-waist wide jeans", "Straight fit jeans", "Boyfriend jeans"]
        if body_type == "Apple":
            return ["Mid-rise straight jeans", "Bootcut jeans"]
        if body_type == "Hourglass":
            return ["Straight fit jeans", "High-waist flare jeans"]
        if body_type == "Rectangle":
            return ["Wide leg jeans", "Boyfriend jeans", "High-waist flare jeans"]
        if body_type == "Inverted triangle":
            return ["Wide leg jeans", "Mom jeans", "Straight fit jeans", "Bootcut jeans"]
        return ["Relaxed fit jeans", "Straight jeans"]

    if gender == "Man":
        if body_type == "Slender":
            return ["Straight jeans", "Slim fit jeans"]
        if body_type == "Broad":
            return ["Straight fit jeans", "Relaxed fit jeans"]
        if body_type == "Athletic":
            return ["Straight jeans", "Tapered jeans"]
        if body_type == "Oval":
            return ["Regular fit jeans", "Straight jeans"]
        return ["Regular fit jeans"]

    return ["Comfort fit jeans"]

# ---------------- OUTFIT LOGIC ----------------

def get_tops(occasion):
    if occasion == "Party / Night out":
        return [("Party outfit", "party wear outfit")]

    if occasion == "Office / Formal":
        return [("Formal outfit", "formal wear outfit")]

    if occasion == "Traditional / Festival / Wedding":
        return [("Ethnic outfit", "ethnic wear outfit")]

    if occasion == "College Wear":
        return [("College outfit", "college outfit fashion")]

    if occasion == "Beach Wear":
        return [("Beach outfit", "beach wear outfit")]

    if occasion == "Gym Wear":
        return [("Gym outfit", "gym wear outfit")]

    return [("Casual outfit", "casual outfit fashion")]

def get_footwear_and_accessories(occasion, age):
    if age == "Newborn (0–1)":
        return [
            ("Baby booties", "newborn socks"),
            ("Baby cap", "newborn cap"),
        ]

    if occasion == "Office / Formal":
        return [
            ("Formal shoes", "formal shoes"),
            ("Office bag", "office bag"),
            ("Watch", "watch"),
        ]

    if occasion == "Party / Night out":
        return [
            ("Stylish footwear", "party footwear"),
            ("Clutch / sling bag", "party bag"),
            ("Accessories", "party accessories"),
        ]

    if occasion == "Gym Wear":
        return [
            ("Training shoes", "gym shoes"),
            ("Gym bag", "gym bag"),
            ("Smartwatch", "fitness watch"),
        ]

    if occasion == "Beach Wear":
        return [
            ("Flip flops", "beach footwear"),
            ("Sunglasses", "sunglasses"),
            ("Beach bag", "beach bag"),
        ]

    return [
        ("Casual footwear", "casual shoes"),
        ("Backpack / handbag", "fashion bag"),
        ("Accessories", "fashion accessories"),
    ]

# ---------------- UI ----------------

st.markdown("## 🎯 Occasion")
occasion = st.selectbox(
    "Select occasion",
    [
        "Casual outing",
        "College Wear",
        "Office / Formal",
        "Party / Night out",
        "Beach Wear",
        "Gym Wear",
        "Traditional / Festival / Wedding",
    ],
)

st.markdown("## 👤 User Profile")
gender = st.selectbox("Gender", ["Woman", "Man", "Kid"])
age = st.selectbox(
    "Age group",
    ["Newborn (0–1)", "Child (2–12)", "Teen", "Adult", "Senior"]
)

# ---------------- BODY TYPE (UNCHANGED) ----------------

st.markdown("## 🧍 Body Type")

if age == "Newborn (0–1)":
    body_type = "Newborn"
    st.info("👶 Body type skipped for newborns.")
else:
    if gender == "Woman":
        body_type = st.selectbox(
            "Select body type",
            ["Pear", "Apple", "Hourglass", "Rectangle", "Inverted triangle"]
        )
    elif gender == "Man":
        body_type = st.selectbox(
            "Select body type",
            ["Slender", "Broad", "Athletic", "Oval"]
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

# ---------------- FINAL AI PICKS ----------------

st.markdown("## ✨ StyleMate’s AI Picks for You")

items = []

# Outfit
items.extend(get_tops(occasion))

# Jeans (ONLY ONCE)
jeans_list = pick_jeans_ai(gender, body_type)
items.append(("AI Selected Jeans", ", ".join(jeans_list)))

# Footwear & Accessories
items.extend(get_footwear_and_accessories(occasion, age))

# ---------------- DISPLAY ----------------

for label, key in items:
    st.markdown(f"### {label}")
    links = get_shopping_links(key, gender)
    cols = st.columns(len(links))
    for col, brand in zip(cols, links):
        col.link_button(brand, links[brand])

st.markdown("---")
st.caption("StyleMate – Rule-based AI Fashion Recommendation MVP")
