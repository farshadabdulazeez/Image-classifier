import os
import pickle
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Load your model and categories
# `settings.MEDIA_ROOT` is the path to the media directory where uploaded files are stored
model_path = os.path.join(settings.MEDIA_ROOT, 'img_model.p')
# Open and load the model from the file using pickle
model = pickle.load(open(model_path, 'rb'))

# Define the categories for prediction. These should match the labels the model was trained on
CATEGORIES = ['sunflower', 'rugby ball leather', 'ice cream cone'] 

def index(request):
    # Check if the request method is POST and if there's an uploaded file in the request
    if request.method == 'POST' and request.FILES.get('image'):
        # Retrieve the uploaded file from the request
        image_file = request.FILES['image']
        
        # Save the uploaded file to the media directory and get its file name
        file_name = default_storage.save(image_file.name, ContentFile(image_file.read()))
        
        # Get the URL and path of the saved file
        file_url = default_storage.url(file_name)
        file_path = default_storage.path(file_name)

        # Debugging: print the URL and path of the uploaded image
        print(f"File URL: {file_url}")
        print(f"File Path: {file_path}")

        # Read the image from the file path
        img = imread(file_path)
        # Resize the image to the dimensions expected by the model (150x150 pixels)
        img_resized = resize(img, (150, 150, 3))
        # Flatten the resized image to a 1D array (for model input)
        flat_data = np.array([img_resized.flatten()])

        # Use the loaded model to predict the category of the image
        y_out = model.predict(flat_data)
        # Retrieve the predicted category from the CATEGORIES list
        predicted_category = CATEGORIES[y_out[0]]

        # Render the index template and pass the predicted category and image URL to it
        return render(request, 'index.html', {'predicted_category': predicted_category, 'image_url': file_url})

    # If the request method is not POST or no file is uploaded, render the index template without predictions
    return render(request, 'index.html')
