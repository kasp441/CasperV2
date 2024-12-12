import pyttsx3

def speak(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties before adding anything to speak
    engine.setProperty('rate', 150)     # Speed of speech
    engine.setProperty('volume', 1)     # Volume level (0-1)

    # Use the engine to speak the text
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Example usage
    text_to_speak = "Hello, this is a test of the text-to-speech module."
    speak(text_to_speak)
