import streamlit as st
import requests
import json
import random

st.set_page_config(page_title="🎨 AI Image Generator", layout="wide")
st.markdown("""
    <style>
        .big-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4a90e2;
        }
        .small-text {
            font-size: 0.9rem;
            color: gray;
        }
        .image-wrapper {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
        }
        .image-container {
            flex: 1 1 300px;
            max-width: 300px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>🖼️ AI Text-to-Image Generator</div>", unsafe_allow_html=True)

st.markdown("<p class='small-text'>Generate stunning images using text prompts powered by AI (Flux API)</p>", unsafe_allow_html=True)

example_prompts = [
    "A majestic dragon curled around a futuristic city at night, glowing neon lights reflecting off its scales",
    "An astronaut meditating on the rings of Saturn with stars swirling in the background, in anime style",
    "A steampunk-style mechanical elephant walking through a Victorian city with gears and smoke",
    "A surreal waterfall flowing from the sky into a floating island, surrounded by glowing butterflies",
    "A cyberpunk samurai standing on a rainy rooftop with neon reflections and a glowing katana",
    "A child drawing in a notebook, and the drawings coming to life in a glowing 3D world around them",
    "An abstract galaxy made of paint splashes and brushstrokes, forming planets and constellations"
]

if st.button("✨ Surprise Me with a Prompt"):
    st.session_state["random_prompt"] = random.choice(example_prompts)

with st.form("image_form"):
    prompt = st.text_input("📝 Enter your image prompt", st.session_state.get("random_prompt", "Iron Man and Spider-Man"))

    style_id = st.selectbox("🎨 Select style", options=[
        (1, "Realistic"),
        (2, "Anime"),
        (3, "Cartoon"),
        (4, "Fantasy")
    ], format_func=lambda x: x[1])[0]

    size = st.selectbox("📐 Select image size", options=[
        ("1-1", "Square (1:1)"),
        ("9-16", "Portrait (9:16)"),
        ("16-9", "Landscape (16:9)")
    ], format_func=lambda x: x[1])[0]

    submitted = st.form_submit_button("🚀 Generate Image")

if submitted:
    st.info("🎨 Generating your image, please wait...")

    url = "https://ai-text-to-image-generator-flux-free-api.p.rapidapi.com/aaaaaaaaaaaaaaaaaiimagegenerator/quick.php"
    headers = {
        "x-rapidapi-key": "80a986d0f0msh587f42439587da4p198a08jsn5da563aac75b",
        "x-rapidapi-host": "ai-text-to-image-generator-flux-free-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "style_id": style_id,
        "size": size
    }

    try:
        images = []
        for _ in range(3):  # Up to 6 images total
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            data = response.json()
            if "final_result" in data and isinstance(data["final_result"], list):
                for img in data["final_result"]:
                    image_url = img.get("origin")
                    if image_url and len(images) < 5:
                        images.append(image_url)
        if images:
            st.success(f"✅ Generated {len(images)} image(s):")
            cols = st.columns(5)
            for i, image_url in enumerate(images):
                with cols[i % 5]:
                    st.image(image_url, caption=f"Image {i+1}", use_container_width=True)
                    st.markdown(f"[📥 Download]({image_url})", unsafe_allow_html=True)
        else:
            st.error("❌ No images returned by API.")

    except Exception as e:
        st.error(f"⚠️ Error occurred: {e}")
