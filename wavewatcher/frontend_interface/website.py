import streamlit as st
import base64
import numpy as np
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

from google.oauth2 import service_account
from google.cloud import storage

#----------Function for adding a background image------------------------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('backgroundimage.png')


#----------Credentials for using Google Cloud storage -------------------------
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])
client = storage.Client(credentials=credentials)


#---------- Retriving contents from csv file in Google Cloud Storage ----------

#Uses st.experimental_memo to only rerun when the query changes or after 1 hour
@st.experimental_memo(ttl=3600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    #Content is retrived as a string
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content


csv = pd.read_csv('gs://waves_surfer_data/prediction/forecast.csv')
bucket_name = "waves_surfer_data"
file_path = "prediction/forecast.csv"

content = read_file(bucket_name, file_path)

#Getting a dictionary from a CSV file that is inside our Google bucket
# dict1 = {}
# list1 = []
# for line in content.strip().split("\n"):
#     list1.append(line)
    # prediction, time, time = line.split(",")
    # dict1[playa] = prediction

st.markdown("""# <span style='color:yellow; font-size:90px; font-family:Graphic'><center>WAVEWATCHER</center></span>
## <span style='color:white'>Choose your break:</span>""", unsafe_allow_html=True)

#----------Code for an API request done by Louis ------------------------------
api = "https://wavewatcher-uy3hohwooq-ez.a.run.app/predict?num_images=15"

@st.cache(suppress_st_warning=True)
def final_message(outcome):
    if outcome == "Good":
        st.markdown(f"<span style='color:white; font-size:40px; font-family:Monaco'>Cowabunga!! Today is a great day to rip some waves! :ocean:</span>", unsafe_allow_html=True)
    if outcome == "Chaotic":
        st.markdown(f"<span style='color:white; font-size:40px; font-family:Monaco'>Too gnarly conditions to surf now my dudes and dudettes. Better waves soon! :no_entry:</span>", unsafe_allow_html=True)
    if outcome == "Flat":
        st.markdown(f"<span style='color:white; font-size:40px; font-family:Monaco'>No waves at the moment, however do not worry, there are a million waves in the world :moyai: </span>", unsafe_allow_html=True)

#from url
patos = Image.open("https://github.com/IamjustNick/wavewatcher/blob/master/wavewatcher/frontend_interface/patos.jpg?raw=true")
new_patos = patos.resize((600, 400))

zarautz =Image.open("https://github.com/IamjustNick/wavewatcher/blob/master/wavewatcher/frontend_interface/zarautz.jpg?raw=true")
new_zarautz = zarautz.resize((600, 400))

hawai = Image.open("https://github.com/IamjustNick/wavewatcher/blob/master/wavewatcher/frontend_interface/hawai.jpg?raw=true")
new_hawai = hawai.resize((600, 400))
#----------Division of the page into 3 columns by Louis ------------------------


columns = st.columns(3)

columns[0].image(new_patos)
if columns[0].button("PREDICTION FOR PATOS"):
    st.markdown(f"""<span style='color:yellow; font-size:40px'><b>Assessing conditions... (don't worry, it may take some time) </b></span>""", unsafe_allow_html=True)
    response = requests.get(api)
    prediction = response.json()
    final_message(prediction['prediction'])
else:
    columns[0].markdown(f"<span style='color:white; font-size:20px'><b>The last prediction at: {csv.iloc[0,2]}</b></span>"
                    f"<p><span style='color:white; font-size:20px'><b>How were the waves: {csv.iloc[0,1]}</b></span></p>"
                    , unsafe_allow_html=True)

columns[1].image(new_zarautz)
with columns[1]:
    if columns[1].button("PREDICTION FOR ZARAUTZ"):
        st.markdown(f"""<span style='color:white; font-size:20px'><b> :rotating_light: :construction: :rotating_light::construction:  <span style='color:white'> Under Construction </span> :rotating_light: :construction: :rotating_light:</b></span>
        """, unsafe_allow_html=True)

columns[2].image(new_hawai)
with columns[2]:
    if columns[2].button("PREDICTION FOR HAWAI"):
        st.markdown(f"""<span style='color:white; font-size:20px'><b> :rotating_light: :construction: :rotating_light::construction:  <span style='color:white'> Under Construction </span> :rotating_light: :construction: :rotating_light:</b></span>
        """, unsafe_allow_html=True)
