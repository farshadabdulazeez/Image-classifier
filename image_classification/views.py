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
model_path = os.path.join(settings.MEDIA_ROOT, 'img_model.p')
model = pickle.load(open(model_path, 'rb'))

CATEGORIES = ['sunflower', 'rugby ball leather', 'ice cream cone']  # Replace with your actual categories

def index(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        file_name = default_storage.save(image_file.name, ContentFile(image_file.read()))
        file_url = default_storage.url(file_name)
        file_path = default_storage.path(file_name)

        # Debugging
        print(f"File URL: {file_url}")
        print(f"File Path: {file_path}")

        img = imread(file_path)
        img_resized = resize(img, (150, 150, 3))
        flat_data = np.array([img_resized.flatten()])

        # Predict using the loaded model
        y_out = model.predict(flat_data)
        predicted_category = CATEGORIES[y_out[0]]

        return render(request, 'index.html', {'predicted_category': predicted_category, 'image_url': file_url})

    return render(request, 'index.html')
