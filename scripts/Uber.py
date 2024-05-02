# https://sigmoidal.ai/
import  numpy    as np
import  pandas   as pd
import streamlit as st
st.set_page_config(page_title='UBER', page_icon='🚕', layout='wide', initial_sidebar_state='expanded')
st.title('Uber PickUps in NYC')
DATE =   'date/time'
DATA =  ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#SIDE
st.sidebar.title('ƊⱭȾɅViƧi🧿Ƞ')
st.sidebar.markdown('''
[![GitHub](  https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](                                 https://github.com/kauefs/)
[![Medium](  https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](                                 https://medium.com/@kauefs)
[![LinkedIn](https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](                               https://www.linkedin.com/in/kauefs/)
[![Python](  https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)
[![License]( https://img.shields.io/github/license/kauefs/StreamLit?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)
            ''')
st.sidebar.text('1 May 2024')
st.sidebar.divider()
st.sidebar.subheader('DashBoard Config:')
hour       = st.sidebar.slider('Hour:', 0, 23, 9)
# Filtered Hour  PlaceHolder:
info       = st.sidebar.empty()
# CheckBox       PlaceHolder:
table      = st.sidebar.empty()
# Filtered Rides PlaceHolder:
success    = st.sidebar.empty()
st.sidebar.divider()
with st.sidebar.container():
     cols = st.columns(3)
     with cols[0]:st.empty()
     with cols[1]:st.markdown('''©2024™''')
     with cols[2]:st.empty()
#MAIN
@st.cache_data
def load_data(nrows):
    data                       = pd.read_csv(DATA, nrows=nrows)
    lowercase                  = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns',inplace=True  )
    data[DATE]                 = pd.to_datetime(data[DATE])
    return data
data=load_data(1000)
FilteredData= data[data[DATE].dt.hour == hour]
info.info(f'''Loading {FilteredData.shape[0]} PickUps…''')
st.subheader('PickUps @ %sh: %s' %  (hour, FilteredData.shape[0]))
st.map(FilteredData)
st.subheader('PickUps by Hour:')
hist  = np.histogram(data[DATE].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist)
if table.checkbox('Show Data', value=False):
    st.subheader('Table Data:')
    success.success(f'''Loading {data.shape[0]} entries…''')
    st.write(data)
