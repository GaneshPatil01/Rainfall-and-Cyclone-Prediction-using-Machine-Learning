import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components
import yaml
from yaml.loader import SafeLoader
from englisttohindi.englisttohindi import EngtoHindi
import openai
import streamlit_authenticator as stauth
openai.api_key = "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"

def gpt3_response(query,tmp = 0.5):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=query,
    temperature=tmp,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)

    return response['choices'][0]['text'].strip()


URL = 'http://e259-202-160-145-20.ngrok-free.app'
google_maps_api_key = "AIzaSyCc_XZ5iXzAS39FCJXjE2zXdM_TY_-bJbw"
df = pd.read_csv('district-wise-rainfall-data-for-india-2014.csv',sep=';')
df.columns = ['INDIAN_STATES_NAME', 'DISTRICTS_NAME', 'DATE', 'FREQUENCY','VARIABLE_NAME', 'VALUE', 'VARIABLE_NOTES']
df['DATE'] = pd.to_datetime(df['DATE'])
s = '% Dep. are the Departures of rainfall from the long period averages of rainfall for the District.'
df = df[df.VARIABLE_NOTES != s]

user_app_choice = st.sidebar.radio(label='Choose',options=['Rainfall','Cyclone'])
if user_app_choice == 'Rainfall':
    st.sidebar.title("Indian Rainfall Prediction App")
    st.image('cap.jpg')
    lang = st.sidebar.radio(label='Choose language',options=['English','Hindi'])

    st.title("Rainfall Prediction using prophet")
    state_categories = sorted(df['INDIAN_STATES_NAME'].unique().tolist())
    if lang == 'Hindi':
        l1 = list(map(lambda x:EngtoHindi(message=x).convert,state_categories))
        state_lang_dict = dict(zip(l1,state_categories))
        state = state_lang_dict[st.selectbox("Select State",l1)]
    else:
        state = st.selectbox("Select State",state_categories)
    df = df[df['INDIAN_STATES_NAME']==state]

    district_categories = sorted(df['DISTRICTS_NAME'].unique().tolist())
    if lang == 'Hindi':
        l2 = list(map(lambda x:EngtoHindi(message=x).convert,district_categories))
        district_lang_dict = dict(zip(l2,district_categories))
        district = district_lang_dict[st.selectbox("Select District",l2)]
    else:
        district = st.selectbox("Select District",district_categories)
    df = df[df['DISTRICTS_NAME'] == district]

    year = int(st.number_input("Select year",min_value=2023))

    month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_idx = list(range(1,13))
    month = dict(zip(month_name,month_idx))
    if lang =='Hindi':
        l3 = list(map(lambda x:EngtoHindi(message=x).convert,month_name))
        month_lang_dict = dict(zip(l3,month_name))
        s = month_lang_dict[st.selectbox("Select month",l3)]
    else:
        s = st.selectbox("Select month",month_name)
    mon = month[s]

    if st.button('Predict'):
        if len(str(mon)) < 2:
            mon = '0'+str(mon)
        date = f'{year}-{mon}-01'
        d = {'state':state,'district':district,'date':date}
        r = requests.post(URL+'/predict', json=d)
        pred = r.json()
        pred = pred['prediction']
        if lang == 'Hindi':
            text = EngtoHindi(message=f'Total rainfall predicted on {s}-{year} in {district},{state} = {pred} mm').convert
            st.write(f"### {text}")
        else:
            st.write(f"### Total rainfall predicted on {s}-{year} in {district},{state} = {pred} mm")

        components.html(f"""<iframe
                            width="600"
                            height="450"
                            style="border:0"
                            loading="lazy"
                            allowfullscreen
                            referrerpolicy="no-referrer-when-downgrade"
                            src="https://www.google.com/maps/embed/v1/place?key={google_maps_api_key}
                            &q={district.replace(" ","")+state.replace(" ","")}">
                            </iframe>""",height=600)
else:
    st.title('Indian cyclone prediction')
    pressure = int(st.number_input("Select pressure in millibar",min_value=0))
    temp = int(st.number_input("Select temperature in degree celcius",min_value=0))
    wind_speed = int(st.number_input("Select wind speed in kph",min_value=0))
    humidity = st.selectbox("Select humidity in millibar",options=['High','Low'])
    if st.button('Predict'):
        param = {'Pressure':f'{pressure} millibar','Humidity':humidity,'Temperature': f'{temp} degree celcius','Wind speed':f'{wind_speed} kph'}
        s = ''
        for i,j in param.items():
            s+=i+': '
            s+=j+'\n'
        query = f"Given following parameter predict whether cyclone will occur or not.\nParameters{s}\n"
        res = gpt3_response(query,tmp = 0.0)
        if 'yes' in res.lower():
            st.error(f'{res}', icon="🚨")
        else:
            st.success(f'{res}', icon="✅")
