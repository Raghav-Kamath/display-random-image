# app.py
from flask import Flask, render_template, request
import webbrowser
from threading import Timer
import os
import random
import re
import math

minimum_threshold=40
attempts=0
minimum_number_of_attempts=3
app = Flask(__name__)

# alter the description according
description = '''Curly hair, short beard, birthmark near moustache , ear piercings ,
Wearing a kada, age around 20, small and sleepy eyes, slightly big forehead'''

#alter the path to the correct image accordingly
correct_image_path = "image1.jpg"

# Function to display the correct image or a random incorrect image
def display_image(keywords):
    
    # Check if input is empty
    if not keywords.strip():
        return None
    global attempts
    attempts+=1
    # convert the input keywords and the description into their respective lists
    input_keywords_List = re.sub("[^\w]", " ", keywords.lower()).split()
    description_List = re.sub("[^\w]", " ", description.lower()).split()

    # Create sets of unique words from input and description
    universal_set_of_unique_words = set(description_List + input_keywords_List)

    # Calculate term frequency for input and description
    input_TF = [input_keywords_List.count(word) for word in universal_set_of_unique_words]
    description_TF = [description_List.count(word) for word in universal_set_of_unique_words]

    # Calculate dot product
    dot_product = sum(input_tf * description_tf for input_tf, description_tf in zip(input_TF, description_TF))

    # Calculate magnitudes of input and description vectors
    input_vector_magnitude = math.sqrt(sum(tf ** 2 for tf in input_TF))
    description_vector_magnitude = math.sqrt(sum(tf ** 2 for tf in description_TF))

    # Calculate match percentage
    if input_vector_magnitude == 0 or description_vector_magnitude == 0:
        return None  # Avoid division by zero
    match_percentage = (dot_product / (input_vector_magnitude * description_vector_magnitude)) * 100
    
    if attempts%minimum_number_of_attempts==0:
        return correct_image_path

    # If the match percentage is above 50%, display the correct image
    if match_percentage >= minimum_threshold:
        return correct_image_path
    else:
        # If keywords do not match, return a random incorrect image
        incorrect_images = [filename for filename in os.listdir("static/images") if filename != correct_image_path]
        return "images/" + random.choice(incorrect_images)

# Define route to display form
@app.route("/", methods=["GET", "POST"])
def index():
    image = None
    if request.method == "POST":
        # Get keywords from the input
        keywords = request.form.get("keywords", "")
        # Get image based on the keywords
        image = display_image(keywords)
    return render_template("result.html", image=image)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(port=5000)
