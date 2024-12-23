from flask import Flask, render_template, request
import pyttsx3

app = Flask(__name__)

# Function to convert text to speech
def text_to_speech(text, voice_index):
    engine = pyttsx3.init()

    # Set properties
    engine.setProperty('rate', 150)  # Speed (words per minute)
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Get available voices and set the selected voice by index
    voices = engine.getProperty('voices')
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)  # Set the voice based on the index

    engine.say(text)
    engine.runAndWait()

# Home page route
@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    voices = []

    # Get available voices for selection
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if request.method == "POST":
        text = request.form.get("text")
        try:
            # Get the voice index (use 0 as default if no selection is made)
            voice_index = int(request.form.get("voice", 0))  # Default to 0 if no voice selected
            if text:
                text_to_speech(text, voice_index)  # Pass the selected voice index
                message = "Speech played successfully!"
        except ValueError:
            message = "Invalid voice selection."

    return render_template("index.html", message=message, voices=voices)

if __name__ == "__main__":
    app.run(debug=True)
