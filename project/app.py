import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
from deep_translator import GoogleTranslator
from playsound import playsound

def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            question = recognizer.recognize_google(audio, language="ur-PK")
            st.write("You said:", question)
            return question
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")
    return None

def translate_to_urdu(text):
    translator = GoogleTranslator(source='en', target='ur')
    translation = translator.translate(text)
    return translation

def text_to_speech(text, lang='ur'):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    temp_file.close()  # Close the file before playing
    st.audio(temp_file.name)
    playsound(temp_file.name)
    os.remove(temp_file.name)

def main():
    st.title("Urdu Voice Assistant")

    input_option = st.radio("Choose input method", ("💬 Text ✍️", "🎙️ Voice 🎤"))

    if input_option == "💬 Text ✍️":
        question = st.text_input("Enter your text")
        if st.button("Submit"):
            if question:
                urdu_text = translate_to_urdu(question)
                # st.write("Translated to Urdu:", urdu_text)
                text_to_speech(urdu_text)
            else:
                st.write("Please enter some text.")
    elif input_option == "🎙️ Voice 🎤":
        st.write("Click to record your voice question:")
        if st.button("Record"):
            question = transcribe_audio()
            if question:
                # st.write("اپ نے کہا:", question)
                text_to_speech(question)

if __name__ == "__main__":
    main()
