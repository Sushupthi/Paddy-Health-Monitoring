from flask import Flask, render_template, request, redirect, url_for, flash
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'your_secret_key_here'

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'tif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files
        # Check if all four images are uploaded
        if 'nir' not in files or 'red' not in files or 'green' not in files or 're' not in files:
            flash('Please upload all four required images.', 'error')
            return redirect(request.url)
        
        nir_file = files['nir']
        red_file = files['red']
        green_file = files['green']
        re_file = files['re']

        if not (allowed_file(nir_file.filename) and allowed_file(red_file.filename) and 
                allowed_file(green_file.filename) and allowed_file(re_file.filename)):
            flash('Invalid file format. Only .TIF files are allowed.', 'error')
            return redirect(request.url)

        # Save files to the upload folder
        nir_path = os.path.join(app.config['UPLOAD_FOLDER'], 'nir.tif')
        red_path = os.path.join(app.config['UPLOAD_FOLDER'], 'red.tif')
        green_path = os.path.join(app.config['UPLOAD_FOLDER'], 'green.tif')
        re_path = os.path.join(app.config['UPLOAD_FOLDER'], 're.tif')
        
        nir_file.save(nir_path)
        red_file.save(red_path)
        green_file.save(green_path)
        re_file.save(re_path)

        # Perform calculations
        ndvi, gndvi, rendvi, reci, crop_health = process_images(nir_path, red_path, green_path, re_path)
        
        # Generate plot images
        ndvi_img = plot_index(ndvi, 'NDVI')
        gndvi_img = plot_index(gndvi, 'GNDVI')
        rendvi_img = plot_index(rendvi, 'RENDVI')
        reci_img = plot_index(reci, 'RECI')

        return render_template('index.html', ndvi_img=ndvi_img, gndvi_img=gndvi_img, 
                               rendvi_img=rendvi_img, reci_img=reci_img, crop_health=crop_health)

    return render_template('index.html')

def process_images(nir_path, red_path, green_path, re_path):
    # Open the NIR, Red, Green, and Red-Edge band images using rasterio
    with rasterio.open(nir_path) as nir_src:
        nir_band = nir_src.read(1).astype(float)

    with rasterio.open(red_path) as red_src:
        red_band = red_src.read(1).astype(float)

    with rasterio.open(green_path) as green_src:
        green_band = green_src.read(1).astype(float)

    with rasterio.open(re_path) as re_src:
        re_band = re_src.read(1).astype(float)

    # Avoid division by zero by using np.errstate
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = (nir_band - red_band) / (nir_band + red_band)
        gndvi = (nir_band - green_band) / (nir_band + green_band)
        rendvi = (nir_band - re_band) / (nir_band + re_band)
        reci = (nir_band / re_band) - 1

    # Set NaNs to 0 or another appropriate value
    ndvi[np.isnan(ndvi)] = 0
    gndvi[np.isnan(gndvi)] = 0
    rendvi[np.isnan(rendvi)] = 0
    reci[np.isnan(reci)] = 0

    # Calculate statistics for each index
    ndvi_mean = np.mean(ndvi)
    gndvi_mean = np.mean(gndvi)
    rendvi_mean = np.mean(rendvi)
    reci_mean = np.mean(reci)

    # Interpret the overall plant health
    crop_health = interpret_health(ndvi_mean, gndvi_mean, rendvi_mean, reci_mean)
    
    return ndvi, gndvi, rendvi, reci, crop_health

def plot_index(index, title):
    fig, ax = plt.subplots()
    cax = ax.imshow(index, cmap='RdYlGn', vmin=-1, vmax=1)
    ax.set_title(title)
    fig.colorbar(cax)

    # Convert plot to PNG image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)

    # Encode PNG to base64
    return base64.b64encode(img.getvalue()).decode('utf8')

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
    
    # GNDVI Interpretation
    if gndvi_value < 0.1:
        health_status.append("Very low chlorophyll content (GNDVI)")
    elif 0.1 <= gndvi_value < 0.5:
        health_status.append("Moderate chlorophyll content (GNDVI)")
    elif gndvi_value >= 0.5:
        health_status.append("High chlorophyll content (GNDVI)")
    
    # RENDVI Interpretation
    if rendvi_value < 0.2:
        health_status.append("Early signs of stress (RENDVI)")
    elif 0.2 <= rendvi_value < 0.5:
        health_status.append("Moderate stress (RENDVI)")
    elif rendvi_value >= 0.5:
        health_status.append("Healthy vegetation, no stress (RENDVI)")

    # RECI Interpretation
    if reci_value < 2:
        health_status.append("Low chlorophyll concentration (RECI)")
    elif 2 <= reci_value < 5:
        health_status.append("Moderate chlorophyll concentration (RECI)")
    elif reci_value >= 5:
        health_status.append("High chlorophyll concentration (RECI)")

    return "; ".join(health_status)

if __name__ == '__main__':
    app.run(debug=True)
