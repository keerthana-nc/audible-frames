Audible Frames is an AI-powered assistive technology designed to help visually impaired individuals experience the world through sound. The project enables users to capture an image, generates a concise and meaningful caption describing the image, and converts the generated text into speech. This solution provides real-time auditory descriptions of the environment, enhancing accessibility and independence for blind users.

How It Works:

Image Capture: The user takes a picture using a mobile device or a camera-enabled system.

Image Captioning: A deep learning model processes the image and generates a short, meaningful caption that describes its contents.

Text-to-Speech Conversion: The caption is passed to a text-to-speech (TTS) model, which converts it into natural-sounding voice output.

Audio Playback: The generated speech is played to the user, providing an intuitive and accessible experience.

Problem It Solves:

Provides real-time descriptions of surroundings for visually impaired individuals.

Enables greater independence by offering auditory assistance in understanding objects, scenes, or text within an image.

Fills the gap in accessibility tools by leveraging AI-powered vision and language processing to enhance daily experiences.

Technologies Used:

Programming Language: Python

Machine Learning Libraries:

Transformers

Torch

TensorFlow Keras

NLTK

LangChain

Frameworks & APIs:

OpenAI API (for image processing and text generation)

LangChain Community

Audio Processing:

Text-to-Speech conversion using OpenAI or other TTS frameworks

Frontend & Deployment:

Streamlit (for user interaction and interface)

Additional Tools:

Pillow (for image handling and processing)

Requests (for API calls)

Python-dotenv (for environment variable management)

Future Scope:

Improving caption accuracy using multimodal learning techniques.

Adding multilingual support for text and speech conversion.

Integrating with wearable devices like smart glasses for real-time feedback.

Enhancing performance for low-end devices with optimized models.

Audible Frames aims to bridge the accessibility gap for the visually impaired, making the world more inclusive and navigable through AI-driven assistive technology.

## Setup

- Ensure you have Python 3.10+ installed.
- Create and populate a `.env` file based on `.env.example`.
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in the project root with the following keys:

```
OPENAI_API_KEY=your_openai_key
HUGGINGFACE_API_TOKEN=your_hf_token
```

## Run locally

```bash
streamlit run app.py
```

Upload a JPG/PNG image. Optionally enable short-story generation in the sidebar. The app will speak either the description or the story and let you download the audio.

## Notes on licensing and attribution

This project is licensed under GPL-3.0 (`LICENSE`). If you create a derivative or redistribute the app:
- Keep the `LICENSE` file and existing copyright notices.
- Disclose your changes and license your derivative under GPL-3.0.
- Provide the full corresponding source when distributing binaries or hosted services, as required by GPL.
