import requests
import json
import base64
import pygame
import pyaudio
import wave
import speech_recognition as sr
import streamlit as st

url = "https://api.convai.com/character/getResponse"

payload = {
    'charID': 'e0c25a94-27a6-11ee-8534-42010a40000b',
    'sessionID': '-1',
    'responseLevel': '5',
    'voiceResponse': 'True'
}

headers = {
    'CONVAI-API-KEY': '1e0cf4d08a1ac807ff3f5e9916d2b559'
}
def record_audio(audio_file_path, duration=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()

    print("Recording...")

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    for _ in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)


    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(audio_file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def convert_audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)  # Record the entire audio file
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return "Error during speech recognition: {0}".format(e)

def play_audio(audio_file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

    # Wait until the playback is finished
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Stop and close the playback
    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def main():
    st.title("Voice-to-Text and Text-to-Voice App")

    user_input = st.text_input("Enter your text or press the microphone button to record voice:", key="input_text")

    if st.button("Start Recording", key="record_button"):
        audio_file_path = 'output_audio.wav'
        record_audio(audio_file_path)
        converted_text = convert_audio_to_text(audio_file_path)

        # Update the text input with the converted text
        st.text_area("Converted Text:", value=converted_text, key="converted_text")

        # Prepare the files for upload
        if user_input:
            files = [('file', ('audio.wav', open(audio_file_path, 'rb'), 'audio/wav'))]

            # Perform the file upload
            response = requests.post(url, headers=headers, data=payload, files=files)
            data = response.json()

            character_response = data["text"]
            st.subheader("Character Response:")
            st.write(character_response)

            decode_string = base64.b64decode(data["audio"])

            with open('audioResponse.wav', 'wb') as f:
                f.write(decode_string)

            # Play the response audio
            play_audio('audioResponse.wav')

if __name__ == "__main__":
    main()
