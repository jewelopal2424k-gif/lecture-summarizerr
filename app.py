import streamlit as st
import whisper
import tempfile
from openai import OpenAI

st.title("Smart Lecture Summarizer")

# 🔹 استخدمي مفتاح OpenAI المخزن في Secrets (آمن للطلاب)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# رفع الملف الصوتي
audio_file = st.file_uploader("Upload your lecture audio (mp3, wav, m4a)")

if audio_file:
    # حفظ الملف مؤقتاً
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    # تحويل الصوت إلى نص باستخدام Whisper
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
