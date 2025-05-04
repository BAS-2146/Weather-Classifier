import streamlit as st
import joblib
import numpy as np
import os  
# Label mapping for output
label_map = {0: 'Cloudy', 1: 'Rainy', 2: 'Snowy', 3: 'Sunny'}

# Encoding maps
cloud_map = {'clear': 0, 'overcast': 1, 'partly cloudy': 2}
season_map = {'Autumn': 0, 'Spring': 1, 'Summer': 2, 'Winter': 3}
location_map = {'coastal': 0, 'inland': 1, 'mountain': 2}

# Load the trained Random Forest model
model = joblib.load("best_rf.pkl")
scaler = joblib.load("scaler.pkl")

# App title
st.title("Weather Classifier")

# Numerical inputs
temperature = st.slider('Temperature (°C)', -20.0, 50.0)
humidity = st.slider('Humidity (%)', 10.0, 100.0)
wind_speed = st.slider('Wind Speed (km/h)', 0.0, 30.0)
precipitation = st.slider('Precipitation (%)', 0.0, 100.0)
pressure = st.slider('Atmospheric Pressure (hPa)', 950.0, 1050.0)
uv_index = st.slider('UV Index', 0, 11)
visibility = st.slider('Visibility (km)', 0.0, 20.0)

# Categorical inputs
cloud_cover = st.selectbox('Cloud Cover', list(cloud_map.keys()))
season = st.selectbox('Season', list(season_map.keys()))
location = st.selectbox('Location', list(location_map.keys()))

# One-hot encoding: Cloud Cover (cloudy, overcast, partly cloudy)
cloud_vector = [0, 0, 0]
if cloud_cover == "cloudy":
    cloud_vector[0] = 1
elif cloud_cover == "overcast":
    cloud_vector[1] = 1
elif cloud_cover == "partly cloudy":
    cloud_vector[2] = 1
# If it's a base case or unknown, keep [0, 0, 0]

# One-hot encoding: Season (Spring, Summer, Winter — Autumn is base case)
season_vector = [0, 0, 0]
if season == "Spring":
    season_vector[0] = 1
elif season == "Summer":
    season_vector[1] = 1
elif season == "Winter":
    season_vector[2] = 1

# One-hot encoding: Location (inland, mountain — coastal is base case)
location_vector = [0, 0]
if location == "inland":
    location_vector[0] = 1
elif location == "mountain":
    location_vector[1] = 1

# Final feature array in correct training order
features = np.array([[temperature,           # 0
                      humidity,              # 1
                      wind_speed,            # 2
                      precipitation,         # 3
                      pressure,              # 4
                      uv_index,              # 5
                      visibility,            # 6
                      *cloud_vector,         # 7–9: cloudy, overcast, partly cloudy
                      *season_vector,        # 10–12: Spring, Summer, Winter
                      *location_vector       # 13–14: inland, mountain
                     ]])





# Prediction
if st.button("Classify"):
    features_scaled  = scaler.transform(features) 
    result = model.predict(features_scaled )[0]
    label = label_map.get(result, "Unknown")
    st.success(f"Predicted Weather Type: {label}")

#  Display file structure
def list_files(startpath):
    tree = ""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        tree += f"{indent}📁 {os.path.basename(root)}\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree += f"{subindent}📄 {f}\n"
    return tree

st.subheader("📂 Project File Structure")
st.code(list_files("."), language="markdown")