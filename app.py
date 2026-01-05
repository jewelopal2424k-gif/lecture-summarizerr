import streamlit as st
import whisper
import tempfile
from openai import OpenAI

st.title("Smart Lecture Summarizer")

# المفتاح مباشر (للتجربة السريعة)
client = OpenAI(api_key="sk-proj-ewlqgXJCEeYWZ1eRququ44s3mdQyUwGMpsPVogr2Pb0JFWJLeGsysBfv9TfmkXhxCtoQmOIXET3BlbkFJmOZdaQKeZw-fv9XWv82zB6EGWSzfLv0ODWpODQDyDj7v-tw1uoG_sIRyoMsbbFHGnd2SZ9oIYA")



audio_file = st.file_uploader("Upload your lecture audio (mp3, wav, m4a)")

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    model = whisper.load_model("base")
    result = model.transcribe(tmp_path)
    text = result["text"]

    if st.button("Summarize"):
        prompt = f"Summarize this lecture in simple English:\n{text}"
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role":"user","content":prompt}]
        )

        st.subheader("Summary:")
        st.write(response.choices[0].message.content)
