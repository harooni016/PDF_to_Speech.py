import streamlit as st
from gtts import gTTS
import io
import pdfplumber
import tempfile

LANG_CODES = {
  "English": "en",
  "Spanish": "es"
}

st.title('📚PDF to Speech By Haroon Sajid📢')

uploaded_file = st.file_uploader('Upload PDF')

if uploaded_file:

  try:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as temp:
      temp.write(uploaded_file.getvalue())
      temp_path = temp.name

    # Open the temporary file with pdfplumber
    with pdfplumber.open(temp_path) as pdf:
      text = ''.join([page.extract_text() for page in pdf.pages])

    with st.sidebar:
      language = st.selectbox('Language', list(LANG_CODES.keys()))
      gender = st.radio('Voice', ['Female'])

    lang_code = LANG_CODES[language]

    tts = gTTS(text=text, lang=lang_code, slow=False)

    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    st.header('Text')
    st.write(text)

    st.header('Audio')
    st.audio(audio_buffer)

  except Exception as e:
    st.error(f"Something went wrong: {e}")

  st.sidebar.header('About') 
  st.sidebar.info('Convert PDF to speech')
