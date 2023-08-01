import requests
import json
import base64
import pygame
import pyaudio
import wave
import speech_recognition as sr

url = "https://api.convai.com/character/getResponse"

payload = {
    'userText': '',
    'charID': 'e0c25a94-27a6-11ee-8534-42010a40000b',
    'sessionID': '-1',
    'voiceResponse': 'True'
}

headers = {
    'CONVAI-API-KEY': ''
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
    
def send_text_input(text_input):
    payload['text'] = text_input
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    if "text" in data:
        character_response = data["text"]
        print("Character Response:", character_response)
        decode_string = base64.b64decode(data.get("audio", ""))
        with open('audioResponse.wav', 'wb') as f:
            f.write(decode_string)
        # Play the response audio
        play_audio('audioResponse.wav')
    else:
        print("No character response received.")

if __name__ == "__main__":
    user_input = ""

    while user_input.lower() != 'q':
        user_input = input("Enter 'a' for audio input, 't' for text input, or 'q' to quit: ")

        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'a':
            # Replace 'output_audio.wav' with the desired path for the recorded audio file
            audio_file_path = 'output_audio.wav'
            # Record audio from the microphone and save it to the specified file
            record_audio(audio_file_path)
            converted_text = convert_audio_to_text(audio_file_path)
            print("Converted Text:", converted_text)
            send_text_input(converted_text)
        elif user_input.lower() == 't':
            text_input = input("Enter your text: ")
            send_text_input(text_input)
        else:
            print("Invalid input. Please try again.")

    print("Goodbye!")
