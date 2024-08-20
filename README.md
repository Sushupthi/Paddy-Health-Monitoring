
# Crop Health Analysis Using NDVI, GNDVI, RENDVI, and RECI

## Overview
This project is designed to calculate various vegetation indices from multispectral images to assess the health of crops. The indices calculated are NDVI (Normalized Difference Vegetation Index), GNDVI (Green Normalized Difference Vegetation Index), RENDVI (Red-Edge Normalized Difference Vegetation Index), and RECI (Red-Edge Chlorophyll Index). These indices help in identifying and interpreting the overall health and condition of the vegetation in the images.

## Vegetation Indices Explained

### 1. NDVI (Normalized Difference Vegetation Index):
- **Formula**: \( 	ext{NDVI} = rac{(	ext{NIR} - 	ext{Red})}{(	ext{NIR} + 	ext{Red})} \)
- **Purpose**: NDVI is used to measure the density and health of vegetation. It compares the reflectance values of the Near-Infrared (NIR) and Red bands of the electromagnetic spectrum.
- **Interpretation**:
  - **NDVI < 0**: Non-vegetative surfaces (e.g., water, barren land).
  - **0 ≤ NDVI < 0.3**: Unhealthy or sparse vegetation.
  - **0.3 ≤ NDVI < 0.6**: Moderate to healthy vegetation.
  - **NDVI ≥ 0.6**: Very healthy, dense vegetation.

### 2. GNDVI (Green Normalized Difference Vegetation Index):
- **Formula**: \( 	ext{GNDVI} = rac{(	ext{NIR} - 	ext{Green})}{(	ext{NIR} + 	ext{Green})} \)
- **Purpose**: GNDVI is particularly sensitive to chlorophyll content in the vegetation and is often used to assess nitrogen levels in plants.
- **Interpretation**:
  - **GNDVI < 0.1**: Very low chlorophyll content, indicating poor health.
  - **0.1 ≤ GNDVI < 0.5**: Moderate chlorophyll content.
  - **GNDVI ≥ 0.5**: High chlorophyll content, indicating healthy vegetation.

### 3. RENDVI (Red-Edge Normalized Difference Vegetation Index):
- **Formula**: \( 	ext{RENDVI} = rac{(	ext{NIR} - 	ext{Red-Edge})}{(	ext{NIR} + 	ext{Red-Edge})} \)
- **Purpose**: RENDVI is used for early stress detection in plants, particularly before visible symptoms appear. It is sensitive to changes in chlorophyll concentration and plant stress.
- **Interpretation**:
  - **RENDVI < 0.2**: Early signs of plant stress.
  - **0.2 ≤ RENDVI < 0.5**: Moderate stress.
  - **RENDVI ≥ 0.5**: Healthy vegetation with no apparent stress.

### 4. RECI (Red-Edge Chlorophyll Index):
- **Formula**: \( 	ext{RECI} = rac{(	ext{NIR})}{(	ext{Red-Edge})} - 1 \)
- **Purpose**: RECI is used to measure chlorophyll concentration in plants. It is effective in identifying areas with varying levels of chlorophyll, which correlates with plant health.
- **Interpretation**:
  - **RECI < 2**: Low chlorophyll concentration.
  - **2 ≤ RECI < 5**: Moderate chlorophyll concentration.
  - **RECI ≥ 5**: High chlorophyll concentration, indicating healthy vegetation.

## Applications
- **Agriculture**: Monitor crop health, detect stress, and optimize the application of water, fertilizers, and pesticides.
- **Environmental Monitoring**: Assess vegetation cover and health over large areas to detect changes due to environmental factors.
- **Research**: Use these indices in studies related to plant physiology, remote sensing, and environmental science.

This project serves as a valuable tool for farmers, agronomists, environmental scientists, and researchers to assess and monitor crop health using multispectral imaging and vegetation indices.
