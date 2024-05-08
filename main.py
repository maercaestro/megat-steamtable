'''
Copyright by Abu Huzaifah Bidin, maercaestro.github.io

This application is designed to extract steam tables data using iapws library.
More features will be added based on requests

'''

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from iapws import iapws97 as steamtable
from PIL import Image

# create a function to convert pressure value

def convert_pressure(pressure, unit=None):
    '''
    A conversion pressure function using typical pressure unit used in the industry. 
    Currently taking in bar, torr, mmHg, atm, psia, and kg/cm2 and convert it to Mpa 
    for usage in iapws module
    '''
    if unit is None:
        unit = 'bar'
    if unit == 'bar':
        pressure = pressure / 10
    elif unit == 'torr':
        pressure = pressure / 7501
    elif unit == 'mmHg':
        pressure = pressure / 7501
    elif unit == 'atm':
        pressure = pressure / 9.869
    elif unit == 'psia':
        pressure = pressure * 0.00689476
    elif unit == 'kg/cm2':
        pressure = pressure * 0.09807
    elif unit == 'kg/cm2g':
        pressure = pressure * 0.1994
    elif unit == 'barg':
        pressure = pressure * 0.2013
    elif unit == 'pa':
        pressure = pressure * 1e-6 

    return pressure

def get_saturated_steam (pressure):
    '''
    Get saturated temperature for steam given pressure in Mpa using iawps97 and return the value in degree C
    
    '''
    tsat = steamtable._TSat_P(pressure)

    return tsat-273.15

# Function to convert pressure to temperature and display result
def convert_and_display(pressure, unit):
    pressure_mpa = convert_pressure(pressure, unit)
    temperature = get_saturated_steam(pressure_mpa)
    st.write(f"Pressure: {pressure} {unit}")
    st.write(f"Temperature: {temperature:.2f} °C")

# Function to iterate over a range of pressures and create a plot
def plot_pressure_range(start_pressure, end_pressure, num_points):
    pressures = np.linspace(start_pressure, end_pressure, num_points)
    temperatures = [get_saturated_steam(convert_pressure(p, 'bar')) for p in pressures]
    plt.plot(pressures, temperatures,marker = 'o')
    plt.xlabel('Pressure (bar)')
    plt.ylabel('Temperature (°C)')
    plt.title('Saturated Steam Curve Against Pressure')
    plt.grid(True)
    st.pyplot()

# Function to iterate over a range of pressures and create a dataframe for download
def create_dataframe(start_pressure, end_pressure, num_points):
    pressures = np.linspace(start_pressure, end_pressure, num_points)
    temperatures = [get_saturated_steam(convert_pressure(p, 'bar')) for p in pressures]
    df = pd.DataFrame({'Pressure (bar)': pressures, 'Temperature (°C)': temperatures})
    return df

# Load the image
image = Image.open('MEGATLogo.png')

# Calculate the new dimensions based on the scale factor
scale_factor = 0.25  # 25% of the original size

# Calculate the new width and height
new_width = int(image.width * scale_factor)
new_height = int(image.height * scale_factor)

# Resize the image
resized_image = image.resize((new_width, new_height))

st.image(resized_image)
# Main Streamlit app
st.title('MEGAT Steam Tables')

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Saturated Temperature", "Download Steam Tables"])

# Single pressure conversion view
if page == "Saturated Temperature":
    
    st.subheader("Get Steam Saturated Temperature")
    # Input fields for pressure value and unit selection
    pressure = st.number_input('Enter Pressure Value')
    unit = st.selectbox('Select Unit', ['bar', 'torr', 'mmHg', 'atm', 'psia', 'kg/cm2', 'kg/cm2g', 'barg', 'pa'])
    # Button to trigger conversion and display result
    if st.button('Get saturated steam temperature'):
        convert_and_display(pressure, unit)

# Pressure range iterator view
elif page == "Download Steam Tables":

    # Disable the PyplotGlobalUseWarning
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Pressure range iterator
    st.subheader("Create Your Own Steam Table Given a Range of Pressure")
    # Input fields for pressure range and number of points
    start_pressure = st.number_input('Start Pressure (bar)')
    end_pressure = st.number_input('End Pressure (bar)')
    num_points = st.number_input('Number of Points', value=10)
    # Button to trigger plot generation
    if st.button('Plot Pressure Range'):
        plot_pressure_range(start_pressure, end_pressure, num_points)
    # Button to trigger dataframe generation
    if st.button('Create DataFrame'):
        df = create_dataframe(start_pressure, end_pressure, num_points)
        st.write(df)
        csv = df.to_csv(index=False)
        st.download_button(label='Download CSV', data=csv, file_name='steam-table.csv', mime='text/csv')
