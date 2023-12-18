import os
import base64
import json
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the fruit model and categories
model = load_model('model/fruitdata.h5')
categories = ['Apple___Black_rot', 'Apple___healthy', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
              'Peach___Bacterial_spot', 'Peach___healthy']

# Load the vegetable model and categories
model_vegetable = load_model('model/vegetabledata.h5')
categories_vegetable = ['Pepper,_bell__Bacterial_spot', 'Pepper,_bell__healthy', 'Potato__Early_blight', 'Potato__healthy', 
                        'Potato__Late_blight', 'Tomato__Bacterial_spot', 'Tomato__Late_blight', 'Tomato__Leaf_Mold', 'Tomato__Septoria_leaf_spot']

# Dictionary of fruit disease recommendations
fruit_recommendations = {
    'Apple___Black_rot': [
        "Prune trees to improve air circulation.",
        "Remove and destroy infected fruit.",
        "Apply fungicides during the growing season."
    ],
    'Apple___healthy': [
        "This is Healthy leaf Of Apple",
        "Continue regular care and monitoring."
    ],
    'Corn_(maize)___Northern_Leaf_Blight': [
        "Rotate crops regularly.",
        "Plant resistant varieties.",
        "Apply fungicides if necessary."
    ],
    'Corn_(maize)___healthy': [
        "This is Healthy leaf Of Corn_(maize)",
        "continue regular care and monitoring."
    ],
    'Peach___Bacterial_spot': [
        "Prune trees to improve air circulation.",
        "Apply copper-based fungicides."
    ],
    'Peach___healthy': [
        "This is Healthy leaf Of Peach" ,
        "continue regular care and monitoring."
    ]
}

# Dictionary of vegetable disease recommendations
vegetable_recommendations = {
    'Pepper,_bell__Bacterial_spot': [
        "Rotate crops regularly.",
        "Avoid overhead watering to reduce splashing.",
        "Apply copper-based fungicides."
    ],
    'Pepper,_bell__healthy': [
        "This is Healthy leaf Of Pepper_bell ",
        "Continue regular care and monitoring."
    ],
    'Potato__Early_blight': [
        "Plant resistant varieties.",
        "Space plants adequately for good air circulation.",
        "Remove and destroy infected leaves.",
        "Apply fungicides containing chlorothalonil or copper."
    ],
    'Potato__healthy': [
        "This is Healthy leaf Of Potato", 
        "continue regular care and monitoring."
    ],
    'Potato__Late_blight': [
        "Plant certified disease-free seedlings.",
        "Remove and destroy infected leaves.",
        "Avoid overhead watering."
    ],
    'Tomato__Bacterial_spot': [
        "Rotate crops regularly.",
        "Avoid overhead watering to reduce splashing.",
        "Apply copper-based fungicides."
    ],
    'Tomato__Late_blight': [
        "Plant certified disease-free seedlings.",
        "Remove and destroy infected leaves.",
        "Avoid overhead watering."
    ],
    'Tomato__Leaf_Mold': [
        "Provide good air circulation.",
        "Avoid overhead watering.",
        "Apply fungicides labeled for leaf mold control."
    ],
    'Tomato__Septoria_leaf_spot': [
        "Provide good air circulation.",
        "Avoid overhead watering.",
        "Apply fungicides labeled for septoria leaf spot control."
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Create the 'temp' directory if it doesn't exist
    if not os.path.exists('temp'):
        os.makedirs('temp')

    # Save the uploaded file to a temporary location
    filename = secure_filename(file.filename)
    temp_path = os.path.join('temp', filename)
    file.save(temp_path)

    # Load and preprocess the image
    img = image.load_img(temp_path, target_size=(128, 128)) 
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Determine the selected model
    selected_model = request.form.get('model')

    if selected_model == 'fruit':
        # Make predictions for fruit model
        predictions = model.predict(img_array)
        predicted_category = categories[np.argmax(predictions)]
        recommendations = fruit_recommendations.get(predicted_category, [])
    elif selected_model == 'vegetable':
        # Make predictions for vegetable model
        predictions = model_vegetable.predict(img_array)
        predicted_category = categories_vegetable[np.argmax(predictions)]
        recommendations = vegetable_recommendations.get(predicted_category, [])

    # Encode the image as base64 for easy display in HTML
    with open(temp_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Delete the temporary uploaded file
    os.remove(temp_path)

    return json.dumps({'prediction': predicted_category, 'recommendations': recommendations, 'image_data': image_data})

@app.route('/result', methods=['GET'])
def result():
    selected_model = request.args.get('model')
    predicted_category = request.args.get('prediction')
    image_data = request.args.get('image_data')

    if selected_model == 'fruit':
        recommendations = fruit_recommendations.get(predicted_category, [])
    elif selected_model == 'vegetable':
        recommendations = vegetable_recommendations.get(predicted_category, [])

    return render_template('result.html', prediction=predicted_category, recommendations=recommendations, image_data=image_data)

if __name__ == '__main__':
    app.run(debug=True)