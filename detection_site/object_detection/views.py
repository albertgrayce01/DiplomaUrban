from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadedImage
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2

def handle_uploaded_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    model = tf.keras.applications.MobileNetV2(weights='imagenet')
    img = tf.keras.applications.mobilenet_v2.preproccess_input(img)
    predictions = model.predict(img)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)
    return decoded_predictions

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            result = handle_uploaded_image(uploaded_image.image.path)
            uploaded_image.result = result
            uploaded_image.save()
            return redirect('results', pk=uploaded_image.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def view_results(request, pk):
    image = UploadedImage.objects.get(pk=pk)
    return render(request, 'results.html', {'image': image})
