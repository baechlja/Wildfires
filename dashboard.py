import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from weather import get_temp,get_wind_speed,get_wind_dir,get_wind_bft
from map import heatmap
from detect import detect_fire

#add CSS sheat
with open('style.css')as f:
 st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

#API Key for OpenWeatherMap
api_key = 'XXX' #replace XXX with your personal api key


# DASHBOARD

st.title('FlameDetect 🔥')
col1, col2= st.columns(2)
#col2.metric('Location', 'DHBW Loerrach', delta=None, delta_color="normal", help=None, label_visibility="visible")
location = col1.selectbox('Location:', ['DHBW Hangstraße','DHBW Marie-Curie-Straße'])

if location == 'DHBW Hangstraße':
    #input geocodes
    lat = 47.6169
    lon = 7.6709
elif 'DHBW Marie-Curie-Straße':
   lat = 47.6086812
   lon = 7.6579978


#FIRE
model_path = "/home/projects/waldbraende/runs/detect/train9/weights/best.pt"
test_image = "/home/projects/waldbraende/test.jpg"
fire = detect_fire(path_to_model=model_path, path_to_image = test_image) # Input from model

if fire == 1:
    fire_geo = [(lat, lon)] # geocodes of firespots
    fire_station = [(47.6027029, 7.6580481)] #geocodes of the next firestation



    #MAP
    heatmap(api_key,lat,lon,fire_geo,fire_station)
else:
   heatmap(api_key,lat,lon)


if fire == 1:
    col2.metric('Status', 'FIRE', delta=None, delta_color="normal", help=None, label_visibility="visible")
else:
   col2.metric('Status', 'NO FIRE', delta=None, delta_color="normal", help=None, label_visibility="visible")

#WEATHER
temp = get_temp(api_key,lat, lon)
wind_speed = get_wind_speed(api_key,lat,lon)
wind_dir = get_wind_dir(api_key,lat,lon)
wind_cat = get_wind_bft(api_key,lat,lon)
wind_type = {0: 'Windstille', 1: 'leiser Zug', 2: 'leichte Brise', 3: 'schwache Brise', 4: 'mäßige Brise',
                    5: 'frische Brise', 6: 'starker Wind', 7: 'steifer Wind', 8: 'stürmischer Wind', 9: 'Stum', 10: 'schwerer Sturm',
                    11: 'orkanartiger Sturm', 12: 'Orkan'}
wind_desc = wind_type[wind_cat]

col1, col2, col3 = st.columns(3)
col1.metric('Temperatur', str(temp) + '°C', delta=None, delta_color="normal", help=None, label_visibility="visible")
col2.metric('Windstärke', str(wind_speed) + ' m/s', delta=None, delta_color="normal", help=None, label_visibility="visible")
col3.metric('Windrichtung', str(wind_dir) + '°', delta=None, delta_color="normal", help=None, label_visibility="visible")

st.metric('Windbeschreibung',str(wind_desc) + ' (' + str(wind_cat) + ' BFT)')

st.markdown('<hr/>', unsafe_allow_html = True)
if fire==1:
    st.info('Notfallpriorität - Feuer befindet sich in Zivilistationsnähe', icon="ℹ️")
components.iframe("http://127.0.0.1:5500/fire.html",width=700, height=500)
