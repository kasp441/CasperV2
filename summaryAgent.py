import speech_recognition as sr
import json
import time
import voiceModule
import Agent
import argparse

# Initialize the ArgumentParser to select the mode
parser = argparse.ArgumentParser(description="Select mode for the chat agent.")
parser.add_argument(
    "-m", "--mode", choices=["voice", "text"], default="voice", 
    help="Choose between 'voice' or 'text' mode."
)
args = parser.parse_args()

# Initialize recognizer for voice
recognizer = sr.Recognizer()

chat_history = []
block = False

def callback(recognizer, audio):
    global chat_history, block  # Declare chat_history and block as global
    print("heard something...")
    try:
        result_json = recognizer.recognize_vosk(audio)
        result = json.loads(result_json)
        text = result.get("text", "")
        print(f"You: {text}")

        if text and not str.isspace(text) and not block:
            # Send user input to the assistant agent
            block = True
            response = Agent.ask_question(text, history=chat_history)
            chat_history = response.chat_history  
            answer = response.summary['content']

            voiceModule.speak(answer)
            block = False
    except Exception as e:
        print(f"Error: {e}")

def text_mode():
    global chat_history
    while True:
        text_input = input("You (text mode): ")
        if text_input.lower() == "exit":
            break
        if text_input and not str.isspace(text_input):
            response = Agent.ask_question(text_input, history=chat_history)
            chat_history = response.chat_history  
            answer = response.summary['content']
            print(f"Agent (text mode): {answer}")

# Mode selection based on command-line argument
if args.mode == "voice":
    # Preload the Vosk model only in voice mode
    print("Preloading Vosk model, please wait...")
    recognizer.recognize_vosk(sr.AudioData(b'', 16000, 2))  # Dummy audio data to trigger model loading

    # Initialize the microphone source for voice mode
    microphone = sr.Microphone()

    print("Adjusting for ambient noise, please wait...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    print("Listening...")

    # Start listening in the background for voice input
    stop_listening = recognizer.listen_in_background(microphone, callback)

    # Keep the script running to continue listening
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping the listener...")
        stop_listening(wait_for_stop=False)

elif args.mode == "text":
    print("Entering text mode...")
    text_mode()
