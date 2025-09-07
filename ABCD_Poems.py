import speech_recognition as sr
import pyttsx3
import random
import os

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speed
voices = engine.getProperty('voices')

# Set to male voice (may vary by system)
for voice in voices:
    if "male" in voice.name.lower() or "david" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Speak function with witty response
def speak(text):
    witty_responses = [
        "Got it!", "On it!", "Here we go!", "Absolutely!",
        "Coming right up!", "You got it!", "Sure thing!", "Of course!"
    ]
    full_text = f"{random.choice(witty_responses)} {text}"
    print(f"Dhruva says: {text}")
    engine.say(full_text)
    engine.runAndWait()

# Poems
poems = [
    """Twinkle, twinkle, little star,
How I wonder what you are!
Up above the world so high,
Like a diamond in the sky.""",
    """Baa, baa, black sheep,
Have you any wool?
Yes sir, yes sir,
Three bags full.""",
    """Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the king's horses and all the king's men,
Couldn't put Humpty together again.""",
    """Jack and Jill went up the hill,
To fetch a pail of water.
Jack fell down and broke his crown,
And Jill came tumbling after.""",
    """The wheels on the bus go round and round,
Round and round, round and round.
The wheels on the bus go round and round,
All through the town.""",
    """Row, row, row your boat,
Gently down the stream.
Merrily, merrily, merrily, merrily,
Life is but a dream.""",
    """Rain, rain, go away,
Come again another day.
Little Johnny wants to play,
Rain, rain, go away."""
]

# Alphabet
alphabet_teach = """A for Apple, B for Ball, C for Cat, D for Dog, 
E for Elephant, F for Fish, G for Goat, H for Hat, 
I for Ice cream, J for Joker, K for Kite, L for Lion, M for Monkey, N for Nest, 
O for Orange, P for Parrot, Q for Queen, R for Rabbit, S for Sun, T for Tiger, 
U for Umbrella, V for Van, W for Watch, X for Xylophone, Y for Yak, Z for Zebra."""

# Listen to user
def listen_command(timeout=5, phrase_time_limit=6):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            print("Didn't catch that.")
            return None
        except sr.RequestError:
            print("Speech service error.")
            return None

# Execute command
def execute_command(command):
    if any(x in command for x in ["exit", "stop", "quit"]):
        speak("Okay,shutting down. See you next time!")
        return "exit"

    if "poem" in command:
        speak(random.choice(poems))

    elif "alphabet" in command:
        speak(alphabet_teach)

    elif "hello" in command or "hi" in command:
        speak("Hey there I'm Dhruva, your witty assistant. What can I help you with today?")

    else:
        speak("Hmm,I haven’t learned that yet.But I'm always getting smarter")

# Run assistant
def run_dhruva_assistant():
    print("Say 'Dhruva' to wake me up... (Say 'exit' anytime to stop)")
    while True:
        wake = listen_command()

        if wake:
            if any(x in wake for x in ["exit", "stop", "quit","shutdown"]):
                speak("Shutting down. Bye bye!")
                break

            if "dhruva" in wake:
                speak("Yes, I'm listening! What's your command?")
                command = listen_command()
                
                if command:
                    result = execute_command(command)
                    if result == "exit":
                        break
                else:
                    speak("I didn’t catch that. Want to try again?")

# Start
if __name__ == "__main__":
    run_dhruva_assistant()
