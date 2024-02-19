# app.py
from flask import Flask, render_template, request
import webbrowser
from threading import Timer
import os
import random

app = Flask(__name__)

# Define predefined correct keywords and corresponding correct image
correct_keywords = ["killer","is", "elon", "the"]
correct_image = "elon_musk.jpg"

# Function to display the correct image or a random incorrect image
def display_image(keywords):
    # Check if input is empty
    if not keywords.strip():
        return None

    # Check if keywords match predefined correct keywords exactly
    input_keywords = set(keywords.lower().split())
    if set(correct_keywords) == input_keywords:
        return correct_image
    # If keywords do not match, return a random incorrect image
    incorrect_images = [filename for filename in os.listdir("static/images") if filename != correct_image]
    return "images/" + random.choice(incorrect_images)

# Define route to display form
@app.route("/", methods=["GET", "POST"])
def index():
    image = None
    correct_image = False
    if request.method == "POST":
        # get keywords from the input
        keywords = request.form.get("keywords", "")
        # get image based on the keywords 
        image = display_image(keywords)
    return render_template("result.html", image=image)

def open_browser():
      webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(port=5000)
