import re
import math
import speech_recognition as sr
import pyttsx3

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print("DHRUVA (Answer):", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=10)
    try:
        command = r.recognize_google(audio)
        print("You (Question):", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

def extract_numbers(text):
    return [float(num) for num in re.findall(r"\d+(?:\.\d+)?", text)]

def parse_input(user_input):
    print("➡️  Parsed Expression:", user_input)

    corrections = {
        'sine': r'sine|sign|sin',
        'cosine': r'cosine|cos|cosign',
        'tangent': r'tangent|tan',
        'log': r'logarithm|log base 10|log of|log',
        'ln': r'natural log|ln',
        'sqrt': r'square root|sqrt',
        'add': r'add|sum|\+|plus|summation of',
        'subtract': r'subtract|minus|\-|difference between',
        'multiply': r'multiply|product|\*|times|into',
        'divide': r'divided by|quotient|/',
        'power': r'power|raised to|to the power of|\*\*',
        'percent': r'percent of|% of|%',
        'factorial': r'factorial'
    }

    for key, pattern in corrections.items():
        if re.search(pattern, user_input):
            numbers = extract_numbers(user_input)
            return key, numbers

    return None, []

def format_number(value):
    if value == int(value):
        return str(int(value))
    else:
        return f"{value:.4f}"

def perform_operation(op, nums):
    try:
        if op == 'add':
            return f"The result is {format_number(nums[0] + nums[1])}" if len(nums) >= 2 else "Please provide two numbers."
        elif op == 'subtract':
            return f"The result is {format_number(nums[0] - nums[1])}" if len(nums) >= 2 else "Please provide two numbers."
        elif op == 'multiply':
            return f"The result is {format_number(nums[0] * nums[1])}" if len(nums) >= 2 else "Please provide two numbers."
        elif op == 'divide':
            return f"The result is {format_number(nums[0] / nums[1])}" if len(nums) >= 2 and nums[1] != 0 else "Cannot divide by zero or missing second number."
        elif op == 'power':
            return f"{format_number(nums[0])} raised to {format_number(nums[1])} is {format_number(math.pow(nums[0], nums[1]))}" if len(nums) >= 2 else "Please provide two numbers."
        elif op == 'sqrt':
            return f"The square root of {format_number(nums[0])} is {format_number(math.sqrt(nums[0]))}" if nums else "Please include a number in your question."
        elif op == 'percent':
            return f"{format_number(nums[0])} percent of {format_number(nums[1])} is {format_number((nums[0]/100) * nums[1])}" if len(nums) >= 2 else "Please provide two numbers."
        elif op == 'factorial':
            return f"The factorial of {int(nums[0])} is {math.factorial(int(nums[0]))}" if nums and nums[0].is_integer() and nums[0] >= 0 else "Factorial is only for non-negative whole numbers."
        elif op == 'log':
            return f"The log of {format_number(nums[0])} is {format_number(math.log10(nums[0]))}" if nums else "Please include a number in your question."
        elif op == 'ln':
            return f"The natural log of {format_number(nums[0])} is {format_number(math.log(nums[0]))}" if nums else "Please include a number in your question."
        elif op == 'sine':
            return f"The sine of {format_number(nums[0])} is {format_number(math.sin(math.radians(nums[0])))}" if nums else "Please include a number in your question."
        elif op == 'cosine':
            return f"The cosine of {format_number(nums[0])} is {format_number(math.cos(math.radians(nums[0])))}" if nums else "Please include a number in your question."
        elif op == 'tangent':
            return f"The tangent of {format_number(nums[0])} is {format_number(math.tan(math.radians(nums[0])))}" if nums else "Please include a number in your question."
        else:
            return "Sorry, I can't do that yet."
    except Exception as e:
        return f"Sorry, I couldn't calculate that: {str(e)}"

# --- Main Loop ---
speak("Hello, I am DHRUVA. Ask your math question.")

while True:
    user_input = listen()

    if 'exit' in user_input or 'quit' in user_input:
        speak("Goodbye!")
        break

    if "dhruva" in user_input:
        op, nums = parse_input(user_input)
        if op and nums:
            result = perform_operation(op, nums)
        elif op and not nums:
            result = "Please include a number in your question."
        else:
            result = "I didn't understand the math operation. Try again with proper numbers and functions."
        speak(result)
    else:
        speak("Please start your question with 'Dhruva'.")
