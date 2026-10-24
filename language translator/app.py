
import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LinguaFlow | Language Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

API_URL = "http://127.0.0.1:5000/translate"
LANGUAGES_URL = "http://127.0.0.1:5000/languages"

LANGUAGE_NAMES = {
    "Arabic": "ar",
    "Albanian": "sq",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Bengali": "bn",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese (Simplified)": "zh-Hans",
    "Chinese (Traditional)": "zh-Hant",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Galician": "gl",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Kyrgyz": "ky",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Malay": "ms",
    "Norwegian": "nb",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Portuguese (Brazil)": "pt-BR",
    "Romanian": "ro",
    "Russian": "ru",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "source_language": "English",
    "target_language": "Spanish",
    "input_text": "",
    "translated_text": "",
    "last_source": "",
    "last_target": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7ff, #eef2ff);
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        text-align: center;
        padding: 25px 10px 30px 10px;
    }

    .hero h1 {
        font-size: 42px;
        font-weight: 800;
        color: #243b72;
        margin-bottom: 8px;
    }

    .hero p {
        color: #596780;
        font-size: 17px;
    }

    .panel-title {
        font-size: 21px;
        font-weight: 700;
        color: #243b72;
        margin: 10px 0;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 12px;
        border: 1px solid #d6dcef;
        background-color: #ffffff;
        font-size: 16px;
        padding: 14px;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
        border: 1px solid #d6dcef;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #536dfe;
        color: #3549bd;
    }

    .info-card {
        background: white;
        border: 1px solid #e0e6f5;
        border-radius: 14px;
        padding: 18px;
        margin: 10px 0 18px 0;
    }

    .footer {
        text-align: center;
        color: #74809a;
        font-size: 13px;
        padding-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🌐 LinguaFlow</h1>
        <p>Break language barriers. Communicate without limits.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-card">
        <b>Welcome to LinguaFlow!</b><br>
        Translate text between supported languages using a
        locally running translation engine.
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# CHECK API CONNECTION AND LANGUAGE SUPPORT
# --------------------------------------------------

@st.cache_data(ttl=60)
def get_supported_languages():
    response = requests.get(LANGUAGES_URL, timeout=5)
    response.raise_for_status()
    data = response.json()

    # Map the supported source-language codes to their targets.
    supported = {}

    for language in data:
        code = language.get("code")
        name = language.get("name")
        targets = language.get("targets", [])

        if code and name:
            supported[code] = {
                "name": name,
                "targets": targets
            }

    return supported


try:
    supported_languages = get_supported_languages()
    api_connected = True

except requests.RequestException:
    supported_languages = {}
    api_connected = False

# --------------------------------------------------
# LANGUAGE SELECTION
# --------------------------------------------------

st.markdown('<div class="panel-title">Choose your languages</div>',
            unsafe_allow_html=True)

available_names = sorted(
    [
        name
        for name, code in LANGUAGE_NAMES.items()
        if code in supported_languages
    ]
)

if not api_connected:
    st.error(
        "Cannot connect to LibreTranslate. "
        "Make sure its server is running at http://127.0.0.1:5000."
    )
    st.stop()

if not available_names:
    st.error("No configured languages were found on the translation server.")
    st.stop()

# Ensure session selections remain valid.
if st.session_state.source_language not in available_names:
    st.session_state.source_language = (
        "English" if "English" in available_names else available_names[0]
    )

if st.session_state.target_language not in available_names:
    st.session_state.target_language = (
        "Spanish" if "Spanish" in available_names else available_names[0]
    )

left, middle, right = st.columns([5, 1, 5])

with left:
    st.selectbox(
        "Source language",
        available_names,
        key="source_language"
    )

with middle:
    st.markdown("<br>", unsafe_allow_html=True)

    swap_clicked = st.button(
        "⇄ Swap",
        use_container_width=True
    )

with right:
    st.selectbox(
        "Target language",
        available_names,
        key="target_language"
    )

# Swap the selected languages.
if swap_clicked:
    current_source = st.session_state.source_language
    current_target = st.session_state.target_language

    if current_target in available_names:
        st.session_state.source_language = current_target

    if current_source in available_names:
        st.session_state.target_language = current_source

    st.rerun()

# --------------------------------------------------
# INPUT AREA
# --------------------------------------------------

source_code = LANGUAGE_NAMES[st.session_state.source_language]
target_code = LANGUAGE_NAMES[st.session_state.target_language]

source_targets = supported_languages[source_code]["targets"]

st.markdown('<div class="panel-title">Enter your text</div>',
            unsafe_allow_html=True)

input_text = st.text_area(
    "Text to translate",
    key="input_text",
    height=190,
    max_chars=10000,
    placeholder="Type or paste the text you want to translate...",
    label_visibility="collapsed"
)

st.caption(f"Characters: {len(input_text)} / 10,000")

# --------------------------------------------------
# ACTION BUTTONS
# --------------------------------------------------

button_left, button_middle, button_right = st.columns([2, 2, 6])

with button_left:
    translate_clicked = st.button(
        "🌐 Translate",
        type="primary",
        use_container_width=True
    )

with button_middle:
    clear_clicked = st.button(
        "🗑 Clear",
        use_container_width=True
    )

if clear_clicked:
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.last_source = ""
    st.session_state.last_target = ""
    st.rerun()

# --------------------------------------------------
# TRANSLATION FUNCTIONALITY
# --------------------------------------------------

if translate_clicked:

    if not input_text.strip():
        st.warning("Please enter some text before translating.")

    elif source_code == target_code:
        st.warning(
            "Choose two different languages to translate your text."
        )

    elif target_code not in source_targets:
        st.error(
            "This source-to-target language combination "
            "is not supported by your local translation engine."
        )

    else:
        payload = {
            "q": input_text.strip(),
            "source": source_code,
            "target": target_code,
            "format": "text"
        }

        try:
            with st.spinner("Translating your text..."):
                response = requests.post(
                    API_URL,
                    data=payload,
                    timeout=60
                )

                if response.status_code == 400:
                    st.error(
                        "The translation request was rejected. "
                        "Check your selected languages and input."
                    )

                elif response.status_code == 403:
                    st.error(
                        "The translation service denied this request."
                    )

                elif response.status_code == 429:
                    st.error(
                        "The service is receiving too many requests. "
                        "Please wait and try again."
                    )

                else:
                    response.raise_for_status()
                    result = response.json()

                    translated = result.get("translatedText")

                    if translated is None:
                        st.error(
                            "The API response did not contain translatedText."
                        )
                    else:
                        st.session_state.translated_text = translated
                        st.session_state.last_source = source_code
                        st.session_state.last_target = target_code
                        st.success("Translation completed successfully!")

        except requests.Timeout:
            st.error(
                "The translation request timed out. "
                "Try a shorter text or try again."
            )

        except requests.ConnectionError:
            st.error(
                "Could not connect to LibreTranslate. "
                "Check that the server is still running."
            )

        except requests.RequestException as error:
            st.error(f"Translation request failed: {error}")

        except ValueError:
            st.error("The translation server returned an invalid response.")

# --------------------------------------------------
# TRANSLATED OUTPUT
# --------------------------------------------------

if st.session_state.translated_text:
    st.markdown(
        '<div class="panel-title">Your translation</div>',
        unsafe_allow_html=True
    )

    st.text_area(
        "Translated text",
        value=st.session_state.translated_text,
        height=190,
        disabled=True,
        key="translated_output"
    )

    st.caption(
        f"Translation: "
        f"{st.session_state.last_source} → "
        f"{st.session_state.last_target}"
    )

    # Copy translation using a Streamlit-supported clipboard component.
    # A downloadable text file is also provided as a reliable fallback.
    copy_column, download_column = st.columns(2)

    with copy_column:
        st.info(
            "To copy the translation, click inside the output box, "
            "press Ctrl+A, then Ctrl+C."
        )

    with download_column:
        st.download_button(
            "⬇ Download Translation",
            data=st.session_state.translated_text,
            file_name="translation.txt",
            mime="text/plain",
            use_container_width=True
        )

    # --------------------------------------------------
    # OPTIONAL TEXT-TO-SPEECH
    # --------------------------------------------------

    st.markdown("#### 🔊 Listen to the translation")

    try:
        from gtts import gTTS

        if st.button("Generate Speech"):
            speech_language = {
                "en": "en",
                "es": "es",
                "fr": "fr",
                "de": "de",
                "hi": "hi",
                "it": "it",
                "ja": "ja",
                "ko": "ko",
                "pt": "pt",
                "ru": "ru",
                "ar": "ar",
                "zh-Hans": "zh-CN",
                "zh-Hant": "zh-TW",
                "nl": "nl",
                "tr": "tr",
            }

            lang = speech_language.get(st.session_state.last_target)

            if not lang:
                st.warning(
                    "Speech generation is not configured for this language."
                )
            else:
                with st.spinner("Generating speech..."):
                    import io

                    audio_buffer = io.BytesIO()

                    tts = gTTS(
                        text=st.session_state.translated_text,
                        lang=lang
                    )

                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)

                    st.audio(audio_buffer, format="audio/mp3")

    except ImportError:
        st.caption(
            "Optional speech feature is not installed yet. "
            "It can be enabled later."
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        LinguaFlow · Language Translation Tool ·
        Powered by Python, Streamlit and LibreTranslate
    </div>
    """,
    unsafe_allow_html=True
)

