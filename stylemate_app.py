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

# ---------------- AI-LIKE JEANS PICKER (UNCHANGED) ----------------
# (your jeans logic stays exactly as you wrote it)

def pick_jeans_ai(gender, body_type, occasion):
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
            return ["Straight jeans", "Regular fit jeans"]
        if body_type == "Oval":
            return ["Regular fit jeans", "Relaxed fit jeans"]
        return ["Regular fit jeans"]

    return ["Comfort fit jeans"]

# ---------------- TOPS LOGIC (NEW & IMPROVED) ----------------

def get_tops(occasion, gender):
    if gender == "Woman":

        # ---------- PARTY ----------
        if "Party" in occasion:
            return [
                ("Fancy party top", "women party top"),
                ("Mini skirt", "women mini skirt"),
                ("Midi skirt", "women midi skirt"),
                ("Maxi skirt", "women maxi skirt"),
                ("Bodycon skirt", "women bodycon skirt"),
                ("Pleated skirt", "women pleated skirt"),
                ("Bodycon dress", "women bodycon dress"),
                ("Mini party dress", "women mini party dress"),
                ("Midi party dress", "women midi party dress"),
                ("Off shoulder dress", "women off shoulder dress"),
            ]

        # ---------- OFFICE ----------
        if "Office" in occasion:
            return [
                ("Formal blouse", "women formal blouse"),
                ("Office shirt", "women formal shirt"),
            ]

        # ---------- TRADITIONAL ----------
        if "Traditional" in occasion:
            return [
                ("Ethnic kurti", "women kurti"),
            ]

        # ---------- COLLEGE ----------
        if "College" in occasion:
            return [
                ("Trendy top", "women trendy top"),
                ("Oversized t-shirt", "women oversized t-shirt"),
                ("Short kurti", "women short kurti"),
                ("Casual shirt", "women casual shirt"),
            ]

        # ---------- BEACH ----------
        if "Beach" in occasion:
            return [
                ("Crop top", "women crop top"),
                ("Breezy shirt", "women beach shirt"),
                ("Maxi beach dress", "women maxi beach dress"),
                ("Slip dress", "women slip dress"),
                ("Wrap dress", "women wrap dress"),
                ("Light bodycon dress", "women summer bodycon dress"),
            ]

        # ---------- GYM ----------
        if "Gym" in occasion:
            return [
                ("Sports bra", "women sports bra"),
                ("Workout t-shirt", "women gym t-shirt"),
                ("Tank top", "women gym tank top"),
            ]

        # ---------- CASUAL ----------
        return [
            ("Casual top", "women casual top"),
            ("T-shirt", "women t-shirt"),
            ("Kurti", "women kurti"),
            ("Short kurti", "women short kurti"),
        ]

    # ---------------- MEN (UNCHANGED) ----------------
    if gender == "Man":
        if "Party" in occasion:
            return [("Party shirt", "men party shirt")]
        if "Office" in occasion:
            return [("Formal shirt", "men formal shirt")]
        if "Traditional" in occasion:
            return [("Ethnic kurta", "men kurta")]
        if "College" in occasion:
            return [
                ("Oversized t-shirt", "men oversized t-shirt"),
                ("Casual shirt", "men casual shirt"),
            ]
        if "Beach" in occasion:
            return [
                ("Printed shirt", "men beach shirt"),
                ("Tank vest", "men tank vest"),
            ]
        if "Gym" in occasion:
            return [
                ("Gym t-shirt", "men gym t-shirt"),
                ("Sleeveless vest", "men gym vest"),
            ]
        return [
            ("Casual t-shirt", "men t-shirt"),
            ("Casual shirt", "men casual shirt"),
        ]

    return []


# ---------------- FOOTWEAR & ACCESSORIES (UNCHANGED) ----------------

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
        "College",
        "Beach look",
        "Gym wear",
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
skin_tone = st.selectbox(
    "Select skin tone",
    ["Light", "Medium", "Tan", "Deep"]
)

# ---------------- TOP PICK ----------------

st.markdown("## ✨ StyleMate’s AI Picks for You")

items = []

# Tops
items.extend(get_tops(occasion, gender))

# Jeans (skip for traditional)
if "Traditional" not in occasion:
    for j in pick_jeans_ai(gender, body_type, occasion):
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
st.caption("StyleMate – Fashion-rule–based AI Recommendation MVP")
