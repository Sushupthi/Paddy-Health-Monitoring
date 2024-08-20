from flask import Flask, request, jsonify, send_file
import os
import numpy as np
import rasterio
from io import BytesIO
from PIL import Image

app = Flask(__name__)

def calculate_indices(nir_band, red_band, green_band, re_band):
    # Same as your previous calculations
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = (nir_band - red_band) / (nir_band + red_band)
        gndvi = (nir_band - green_band) / (nir_band + green_band)
        rendvi = (nir_band - re_band) / (nir_band + re_band)
        reci = (nir_band / re_band) - 1

    ndvi[np.isnan(ndvi)] = 0
    gndvi[np.isnan(gndvi)] = 0
    rendvi[np.isnan(rendvi)] = 0
    reci[np.isnan(reci)] = 0

    return ndvi, gndvi, rendvi, reci

def normalize_and_convert(image_array):
    normalized = np.clip(255 * (image_array - np.min(image_array)) / (np.max(image_array) - np.min(image_array)), 0, 255)
    return normalized.astype(np.uint8)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Read uploaded files
    green_file = request.files['green_image']
    red_file = request.files['red_image']
    re_file = request.files['re_image']
    nir_file = request.files['nir_image']

    with rasterio.open(BytesIO(green_file.read())) as green_src, \
         rasterio.open(BytesIO(red_file.read())) as red_src, \
         rasterio.open(BytesIO(re_file.read())) as re_src, \
         rasterio.open(BytesIO(nir_file.read())) as nir_src:

        green_band = green_src.read(1).astype(float)
        red_band = red_src.read(1).astype(float)
        re_band = re_src.read(1).astype(float)
        nir_band = nir_src.read(1).astype(float)

    ndvi, gndvi, rendvi, reci = calculate_indices(nir_band, red_band, green_band, re_band)

    # Interpret health
    health_status = interpret_health(np.mean(ndvi), np.mean(gndvi), np.mean(rendvi), np.mean(reci))

    # Convert to JPEG
    output_images = {}
    for index_name, index_data in {'NDVI': ndvi, 'GNDVI': gndvi, 'RENDVI': rendvi, 'RECI': reci}.items():
        img = Image.fromarray(normalize_and_convert(index_data))
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        output_images[index_name] = f'data:image/jpeg;base64,{img_io.read().decode("utf-8")}'

    return jsonify({'health_status': health_status, 'images': output_images})

def interpret_health(ndvi_value, gndvi_value, rendvi_value, reci_value):
    health_status = []
    
    # NDVI Interpretation
    if ndvi_value < 0:
        health_status.append("Non-vegetative surface (NDVI)")
    elif 0 <= ndvi_value < 0.3:
        health_status.append("Unhealthy or sparse vegetation (NDVI)")
    elif 0.3 <= ndvi_value < 0.6:
        health_status.append("Moderate to healthy vegetation (NDVI)")
    elif ndvi_value >= 0.6:
        health_status.append("Very healthy, dense vegetation (NDVI)")
    
    # GNDVI Interpretation (Chlorophyll/Nitrogen)
    if gndvi_value < 0.1:
        health_status.append("Very low chlorophyll content (GNDVI)")
    elif 0.1 <= gndvi_value < 0.5:
        health_status.append("Moderate chlorophyll content (GNDVI)")
    elif gndvi_value >= 0.5:
        health_status.append("High chlorophyll content (GNDVI)")

    # RENDVI Interpretation (Early Stress Detection)
    if rendvi_value < 0.2:
        health_status.append("Early signs of stress (RENDVI)")
    elif 0.2 <= rendvi_value < 0.5:
        health_status.append("Moderate stress (RENDVI)")
    elif rendvi_value >= 0.5:
        health_status.append("Healthy vegetation, no stress (RENDVI)")

    # RECI Interpretation (Chlorophyll Concentration)
    if reci_value < 2:
        health_status.append("Low chlorophyll concentration (RECI)")
    elif 2 <= reci_value < 5:
        health_status.append("Moderate chlorophyll concentration (RECI)")
    elif reci_value >= 5:
        health_status.append("High chlorophyll concentration (RECI)")

    return "; ".join(health_status)
    # Your previous interpret_health function
    #pass

if __name__ == '__main__':
    app.run(debug=True)
