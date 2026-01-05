import streamlit as st
import whisper
from openai import OpenAI
import tempfile

st.title("Smart Lecture Summarizerr")

# 🔹 ضع مفتاح OpenAI هنا مباشرة
client = OpenAI(api_key="sk-proj-ewlqgXJCEeYWZ1eRququ44s3mdQyUwGMpsPVogr2Pb0JFWJLeGsysBfv9TfmkXhxCtoQmOIXET3BlbkFJmOZdaQKeZw-fv9XWv82zB6EGWSzfLv0ODWpODQDyDj7v-tw1uoG_sIRyoMsbbFHGnd2SZ9oIYA")

# رفع الملف الصوتي
audio_file = st.file_uploader("Upload your lecture audio (mp3, wav, m4a)")

if audio_file:
    # حفظ الملف مؤقتاً
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    # تحويل الصوت لنص باستخدام Whisper
    model = whisper.load_model("base")
    result = model.transcribe(tmp_path)
    text = result["text"]

    # زر التلخيص
    if st.button("Summarize"):
        prompt = f"Summarize this lecture in simple English:\n{text}"

        # طلب التلخيص من OpenAI GPT
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role":"user","content":prompt}]
        )

        st.subheader("Summary:")
        st.write(response.choices[0].message.content)
