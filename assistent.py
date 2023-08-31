import pyaudio
import speech_recognition as sr
import pyttsx3
import openai
import uuid
import time

api_key = ""
lang = 'en'

openai.api_key = api_key

guy = ""
is_activated = False  # Flag to indicate if the AI is activated

def speak_response(response_text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 200)  # Adjust the speaking rate (increase for faster speech)
    engine.say(response_text)
    engine.runAndWait()

def check_stop_command(response_text):
    stop_keywords = ["stop", "cancel", "quit", "exit", "end"]  # Add more keywords as needed
    for keyword in stop_keywords:
        if keyword in response_text.lower():
            return True
    return False

def get_audio():
    global guy
    global is_activated

    r = sr.Recognizer()
    with sr.Microphone(device_index=2) as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise before capturing audio

        if not is_activated:
            print("Listening for Jarvis...")
            audio = r.listen(source)
        else:
            print("Listening...")
            audio = r.listen(source)

    try:
        said = r.recognize_google(audio)
        print("You said:", said)
        guy = said

        if not is_activated and "Jarvis" in said:
            print("Jarvis activated.")
            is_activated = True
            return

        if is_activated and "Jarvis" not in said:
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": said}])
            text = completion.choices[0].message.content

            # Check if the AI response contains the stop command
            if check_stop_command(text):
                print("AI response stopped.")
                is_activated = False
            else:
                # Speak the AI's response
                speak_response(text)
                time.sleep(2)  # Time-out period (2 seconds) after each response

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError:
        print("Sorry, my speech service is unavailable at the moment.")

if __name__ == "__main__":
    try:
        while True:
            if "stop" in guy:
                break
            get_audio()
    except KeyboardInterrupt:
        print("Listening stopped.")
