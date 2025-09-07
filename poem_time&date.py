import speech_recognition as sr
from gtts import gTTS
from IPython.display import Audio, display
import random
from datetime import datetime
import pyaudio

# Speak function
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "dhruva_speak.mp3"
    tts.save(filename)
    return Audio(filename, autoplay=True)

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
    And Jill came tumbling after."""
]

# Alphabets
alphabet_teach = """A for Apple, B for Ball, C for Cat, D for Dog, 
E for Elephant, F for Fish, G for Goat, H for Hat, 
I for Ice cream, J for Joker, K for Kite, L for Lion, M for Monkey, N for Nest, 
O for Orange, P for Parrot, Q for Queen, R for Rabbit, S for Sun, T for Tiger, 
U for Umbrella, V for Van, W for Watch, X for Xylophone, Y for Yak, Z for Zebra."""

# Colors
colors_teach = """Red like an apple, Blue like the sky, Green like the grass, 
Yellow like the sun, Orange like an orange fruit, Purple like grapes, 
Pink like cotton candy, Black like the night, White like snow."""

# Listen command function
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dhruva is listening... 🎤")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand. 😔")
        return None
    except sr.RequestError:
        print("Sorry, could not request results from Google Speech Recognition. 😔")
        return None

# Main Dhruva function
def dhruva_listen_and_act():
    command = listen_command()

    if command:
        if "poem" in command:
            chosen_poem = random.choice(poems)
            print("\nReciting a poem...\n")
            print(chosen_poem)
            return speak(chosen_poem)
        
        elif "time" in command or "date" in command:
            now = datetime.now()
            current_time = now.strftime("%I:%M %p")
            current_date = now.strftime("%d %B, %Y")
            reply = f"The current time is {current_time}, and today's date is {current_date}."
            print("\nTelling the time and date...\n")
            return speak(reply)
        
        elif "alphabet" in command:
            print("\nTeaching alphabets...\n")
            return speak(alphabet_teach)
        
        elif "color" in command or "colour" in command:
            print("\nTeaching colors...\n")
            return speak(colors_teach)
        
        elif "hello" in command or "hi" in command:
            greeting = "Hello! I am Dhruva, your smart friend. How can I help you today?"
            print("\nGreeting user...\n")
            return speak(greeting)
        
        else:
            print("\nDhruva says: Sorry, I can only recite poems, tell time, teach alphabets and colors for now.")
            return speak("Sorry, I can only recite poems, tell time, teach alphabets and colors for now.")
    else:
        return speak("I didn't catch that. Please try again.")

# Run Dhruva
output = dhruva_listen_and_act()
display(output)