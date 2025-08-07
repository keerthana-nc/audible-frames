import os
import tempfile
from typing import Any, Optional

import requests
import streamlit as st
from dotenv import find_dotenv, load_dotenv

from utils.custom import css_code

import base64
from openai import OpenAI


load_dotenv(find_dotenv())
HUGGINGFACE_API_TOKEN: Optional[str] = os.getenv("HUGGINGFACE_API_TOKEN")
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")


def require_env(var_name: str, value: Optional[str]) -> None:
    if not value:
        st.error(
            f"Missing required environment variable `{var_name}`. Please set it in your `.env` file.")
        st.stop()


def encode_image_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def generate_text_from_image(file_path: str) -> str:
    """
    Describe the image using OpenAI vision model.
    """
    require_env("OPENAI_API_KEY", OPENAI_API_KEY)

    client = OpenAI(api_key=OPENAI_API_KEY)
    base64_image = encode_image_to_base64(file_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the main features from this image: describe objects, colors, and any visible text. If the image is purely text, just extract that text."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content or ""


def generate_story_from_text(context: str, max_words: int = 50) -> str:
    """
    Create a short story from the context using OpenAI (no LangChain).
    """
    require_env("OPENAI_API_KEY", OPENAI_API_KEY)

    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = (
        "You are a talented storyteller. Create a vivid story with at most "
        f"{max_words} words from the given context.\n\nCONTEXT: "
        f"{context}\nSTORY:"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.9,
    )
    return response.choices[0].message.content or ""


def generate_speech_from_text(message: str) -> str:
    """
    Generate speech using the ESPnet TTS model on HuggingFace Inference API.

    Returns the path to the generated audio file.
    """
    require_env("HUGGINGFACE_API_TOKEN", HUGGINGFACE_API_TOKEN)

    api_url: str = (
        "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    )
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Accept": "audio/flac",
        "Content-Type": "application/json",
    }
    payload = {"inputs": message}

    resp = requests.post(api_url, headers=headers, json=payload, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(
            f"TTS request failed with status {resp.status_code}: {resp.text[:200]}"
        )

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".flac", prefix="tts_")
    with open(tmp_file.name, "wb") as f:
        f.write(resp.content)
    return tmp_file.name


def main() -> None:
    st.set_page_config(page_title="Audible Frames", page_icon="🖼️")
    st.markdown(css_code, unsafe_allow_html=True)

    st.header("Audible Frames")

    with st.sidebar:
        st.subheader("Options")
        enable_story = st.checkbox("Generate short story from description", value=False)
        max_story_words = st.slider("Max story words", min_value=20, max_value=120, value=50, step=5)

    uploaded_file: Any = st.file_uploader(
        "Please choose an image to upload", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        st.info("Upload a JPG or PNG image to begin.")
        return

    # Persist uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getbuffer())
        image_path = tmp.name

    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    try:
        with st.spinner("Analyzing image..."):
            scenario: str = generate_text_from_image(image_path)

        story: Optional[str] = None
        if enable_story and scenario:
            with st.spinner("Writing short story..."):
                story = generate_story_from_text(scenario, max_words=max_story_words)

        with st.spinner("Generating speech..."):
            audio_path = generate_speech_from_text(story or scenario)

        with st.expander("Generated image description"):
            st.write(scenario or "No description generated.")

        if story is not None:
            with st.expander("Generated short story"):
                st.write(story)

        st.audio(audio_path)
        st.download_button("Download audio", data=open(audio_path, "rb").read(), file_name=os.path.basename(audio_path), mime="audio/flac")

    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
