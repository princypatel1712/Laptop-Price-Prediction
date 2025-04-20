import streamlit as st
import pickle
import pandas as pd
import numpy as np
import sklearn 
import os

pipe = pickle.load(open('model.pkl','rb'))
df = pd.read_csv('clean_data.csv')
# Background image using CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://wallpapercave.com/wp/wp5320845.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title('Laptop Price Predictor')


#brand
brand = st.selectbox('Brand',df['Company'].unique())

# type of laptop
type = st.selectbox('Type',df['TypeName'].unique())

#Ram
ram = st.selectbox('Ram',sorted(list(df['Ram'].unique())))

#Weight
weigth = st.number_input('Weight In KG',min_value=0)

#Touchscreen
touchscreen = st.selectbox('Touchscreen',['Yes','No'])

#IPS
ips = st.selectbox('IPS Display',['Yes','No'])

#Screen Size
inch = st.number_input('Screen Size In Inch',min_value=1)
#resolution
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])
# tpi = resolution/inch

#cpu
cpu =st.selectbox('CPU',df['Cpu'].unique())

#hdd
hdd =st.number_input('HDD In GB',min_value=0)

#ssd
ssd =st.number_input('SSD In GB',min_value=0)

#gpu
gpu =st.selectbox('GPU',df['Gpu'].unique())

#os
os =st.selectbox('OS',df['OpSys'].unique())

#speed
speed =st.selectbox('Speed In GHz',sorted(df['Speed'].unique()))
if st.button('Predict Price'):
    try:
        # Encode touchscreen and IPS
        touchscreen_val = 1 if touchscreen == 'Yes' else 0
        ips_val = 1 if ips == 'Yes' else 0

        # Calculate PPI
        x_res = int(resolution.split('x')[0])
        y_res = int(resolution.split('x')[1])
        ppi = ((x_res ** 2 + y_res ** 2) ** 0.5) / inch

        # Prepare input as DataFrame (not NumPy array!)
        input_df = pd.DataFrame([{
    'Company': brand,
    'TypeName': type,
    'Cpu': cpu,
    'Ram': ram,
    'Gpu': gpu,
    'OpSys': os,
    'Weight': weigth,
    'TouchScreen': touchscreen_val,   # ← Fixed
    'IPS': ips_val,                  # ← Fixed
    'ppi': ppi,                      # ← Fixed
    'Speed': speed,
    'HDD': hdd,
    'SSD': ssd
}])

        # Predict (assuming model is trained on log prices)
        prediction = pipe.predict(input_df)
        final_price = np.round(np.exp(prediction[0]), 0)

        st.success(f"Estimated Laptop Price: ₹{final_price}")
        st.title(f"Price For Laptop Will Be Rs. {final_price}")

    except Exception as e:
        st.error(f"Error during prediction: {e}")
